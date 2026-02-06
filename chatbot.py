import os
import sys
from google import genai  # Modern 2026 SDK
from google.genai import types
from dotenv import load_dotenv, find_dotenv
from config import attacker_profiles
from utils import sanitize_input

from rich.console import Console
console = Console()

# ─── Environment Validation ─────────────────────────────────────────────
def validate_environment():
    try:
        env_path = find_dotenv(raise_error_if_not_found=True)
        load_dotenv(env_path, encoding='utf-8-sig')
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key or len(api_key) < 20:
            console.print("[bold red]❌ Invalid GEMINI_API_KEY[/bold red]")
            return False

        console.print("[bold green]✅ Environment validation successful[/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]🔥 Env Error:[/bold red] {str(e)}")
        return False

# ─── Gemini Initialization ──────────────────────────────────────────────
def initialize_gemini_client():
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        console.print("[bold green]✅ Gemini Client initialized successfully[/bold green]")
        return client
    except Exception as e:
        console.print(f"[bold red]🚨 Initialization failed:[/bold red] {str(e)}")
        sys.exit(1)

# ─── Generate Gemini Response ───────────────────────────────────────────
def generate_response(client, prompt, tactic):
    """Generates a single response for a specific tactic."""
    try:
        system_msg = attacker_profiles[tactic]["system_prompt"]
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_msg,
                temperature=0.7,
                max_output_tokens=2048 # Increased to prevent cut-offs
            )
        )

        if response and response.text:
            return response.text.strip()
        return "❓ No response text returned. Check safety filters."

    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# ─── Unified Attack Orchestrator ───────────────────────────────────────
def generate_full_attack_chain(client, master_goal):
    """
    Sequences all three phases automatically, passing context 
    between them to maintain logic consistency.
    """
    results = {}
    
    # Pass 1: Reconnaissance
    recon_out = generate_response(client, master_goal, "recon_gatherer")
    results["recon_gatherer"] = recon_out
    
    # Pass 2: Initial Access (Uses Recon data as context)
    access_prompt = f"Target Goal: {master_goal}\n\nBased on these Recon findings: {recon_out}"
    access_out = generate_response(client, access_prompt, "phishing_specialist")
    results["phishing_specialist"] = access_out
    
    # Pass 3: Execution (Uses Access data as context)
    exec_prompt = f"Target Goal: {master_goal}\n\nBased on this Access method: {access_out}"
    exec_out = generate_response(client, exec_prompt, "execution_simulator")
    results["execution_simulator"] = exec_out
    
    return results

# ─── Entry Point ────────────────────────────────────────────────────────
client_instance = None
if validate_environment():
    client_instance = initialize_gemini_client()

def get_response(user_input: str, mode="single", tactic="recon_gatherer") -> any:
    """
    Entry point for Flask. Supports single-phase or full-chain mode.
    """
    if not client_instance:
        return "🚫 Model not initialized."

    clean_input = sanitize_input(user_input)
    if clean_input.startswith("[BLOCKED]"):
        return clean_input

    if mode == "full_chain":
        return generate_full_attack_chain(client_instance, clean_input)
    
    return generate_response(client_instance, clean_input, tactic)

    