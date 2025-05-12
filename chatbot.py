import os
import sys
import google.generativeai as genai
from google.generativeai import GenerationConfig
from dotenv import load_dotenv, find_dotenv
from config import attacker_profiles  # Ensure config.py is in the same directory
from utils import sanitize_input, display_ethical_warning

from rich.console import Console
from rich.rule import Rule

console = Console()

# ─── Environment Validation ─────────────────────────────────────────────
def validate_environment():
    try:
        env_path = find_dotenv(raise_error_if_not_found=True)
        console.print(f"🔍 Loading .env from: [italic]{env_path}[/italic]")

        with open(env_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            if "GEMINI_API_KEY=" not in content:
                console.print("[bold red]❌ Invalid .env format - must contain GEMINI_API_KEY[/bold red]")
                return False

        load_dotenv(env_path, encoding='utf-8-sig')
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key or len(api_key) < 20:
            console.print("[bold red]❌ Invalid GEMINI_API_KEY format or missing[/bold red]")
            return False

        console.print("[bold green]✅ Environment validation successful[/bold green]")
        return True

    except Exception as e:
        console.print(f"[bold red]🔥 Error during environment validation:[/bold red] {str(e)}")
        console.print("[bold yellow]Please ensure you have a .env file with GEMINI_API_KEY=YOUR_API_KEY[/bold yellow]")
        return False

# ─── Gemini Initialization ──────────────────────────────────────────────
def initialize_gemini_model():
    model_name = None
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        genai.configure(api_key=api_key)

        model_name = "models/gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)
        console.print(f"[bold green]✅ Gemini model '{model_name}' initialized successfully[/bold green]")
        return model

    except Exception as e:
        console.print(f"[bold red]🚨 Gemini model initialization failed:[/bold red] {str(e)}")
        console.print("[bold yellow]Ensure GEMINI_API_KEY is valid and model name is accessible.[/bold yellow]")
        if model_name:
            console.print(f"[bold yellow]Attempted model:[/bold yellow] {model_name}")
        sys.exit(1)

# ─── Generate Gemini Response ───────────────────────────────────────────
def generate_response(model, prompt, tactic):
    try:
        system_msg = attacker_profiles[tactic]["system_prompt"]
        full_prompt = f"{system_msg}\n\nUser Request: {prompt}"

        generation_config = GenerationConfig(
            temperature=0.7,
            max_output_tokens=800
        )

        response = model.generate_content(
            full_prompt,
            generation_config=generation_config
        )

        if response and response.text:
            return response.text.strip()
        elif response and response.prompt_feedback and response.prompt_feedback.block_reason:
            block_reason = response.prompt_feedback.block_reason.name
            return f"🚫 Blocked by safety filters. Reason: {block_reason}"
        else:
            return "❓ No response text returned."

    except Exception as e:
        error_type = type(e).__name__
        return f"⚠️ API Error ({error_type}): {str(e)}"

# ─── Flask Chatbot-Compatible Response ──────────────────────────────────
# This is the function Flask will use
model_instance = None
if validate_environment():
    model_instance = initialize_gemini_model()

def get_response(user_input: str) -> str:
    if not model_instance:
        return "🚫 Model not initialized."

    clean_input = sanitize_input(user_input)
    if clean_input.startswith("[BLOCKED]"):
        return clean_input

    if any(k in clean_input.lower() for k in ["phish", "email", "social engineer"]):
        tactic = "phishing_attacker"
    elif any(k in clean_input.lower() for k in ["osint", "information", "data", "public source"]):
        tactic = "osint_gatherer"
    else:
        tactic = "osint_gatherer"

    return generate_response(model_instance, clean_input, tactic)
