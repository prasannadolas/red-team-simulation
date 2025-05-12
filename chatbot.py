import os
import sys
import google.generativeai as genai
from google.generativeai import GenerationConfig
from dotenv import load_dotenv, find_dotenv
from config import attacker_profiles # Ensure config.py is in the same directory
from utils import sanitize_input, display_ethical_warning # Ensure utils.py is in the same directory

# Import rich components for the interactive interface in main
from rich.console import Console
from rich.rule import Rule
# from rich.style import Style # Not strictly needed if using tags like [bold]

# Create a Console instance for rich printing - used throughout if needed, but mainly in main
console = Console()

def validate_environment():
    """Validate environment configuration with BOM detection for GEMINI_API_KEY"""
    try:
        env_path = find_dotenv(raise_error_if_not_found=True)
        console.print(f"🔍 Loading .env from: [italic]{env_path}[/italic]")

        # Read with BOM handling and check for GEMINI_API_KEY
        with open(env_path, 'r', encoding='utf-8-sig') as f:
            content = f.read() # Read full content to check for key presence
            if "GEMINI_API_KEY=" not in content:
                console.print("[bold red]❌ Invalid .env format - must contain GEMINI_API_KEY[/bold red]")
                return False

        load_dotenv(env_path, encoding='utf-8-sig')
        api_key = os.getenv("GEMINI_API_KEY")

        # Basic check: Gemini API keys are usually long
        if not api_key or len(api_key) < 20: # Adjusted length check
            console.print("[bold red]❌ Invalid GEMINI_API_KEY format or missing[/bold red]")
            return False

        console.print("[bold green]✅ Environment validation successful[/bold green]")
        return True

    except Exception as e:
        console.print(f"[bold red]🔥 Error during environment validation:[/bold red] {str(e)}")
        console.print("[bold yellow]Please ensure you have a .env file with GEMINI_API_KEY=YOUR_API_KEY[/bold yellow]")
        return False

def initialize_gemini_model():
    """Configure Google Generative AI and get the model with proper error handling"""
    model_name = None # Define here to be accessible in the except block
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
             raise ValueError("GEMINI_API_KEY not found in environment variables.")

        genai.configure(api_key=api_key)

        # Use the model name identified as available from your list_models.py output
        # We are using gemini-1.5-flash as it has separate quotas from gemini-1.5-pro
        model_name = "models/gemini-1.5-flash" # Using the gemini-1.5-flash alias
        # You could also use "models/gemini-1.5-flash-latest" or a specific dated version
        # If you prefer the potentially more capable Pro model and have quota, use "models/gemini-1.5-pro"

        model = genai.GenerativeModel(model_name)
        console.print(f"[bold green]✅ Gemini model '{model_name}' initialized successfully[/bold green]")
        return model

    except Exception as e:
        console.print(f"[bold red]🚨 Gemini model initialization failed:[/bold red] {str(e)}")
        console.print("[bold yellow]Please ensure your GEMINI_API_KEY is correct and the model name is valid and available in your region.[/bold yellow]")
        if model_name: # Only print if model_name was set before the error
            console.print(f"[bold yellow]Attempted to load model:[/bold yellow] {model_name}")
        console.print("[bold yellow]Run list_models.py script to see available models.[/bold yellow]")
        sys.exit(1)

def generate_response(model, prompt, tactic):
    """Generate AI response using Gemini model with error handling and increased token limit"""
    try:
        system_msg = attacker_profiles[tactic]["system_prompt"]

        # Combine system message and user prompt for generate_content
        full_prompt = f"{system_msg}\n\nUser Request: {prompt}"

        # Define generation configuration
        generation_config = genai.GenerationConfig(
            temperature=0.7, # Adjust temperature (0.0 to 1.0) for creativity vs. focus
            max_output_tokens=800 # <--- Increased value for longer responses
            # Add other config params here if needed, e.g., top_p, top_k
        )

        response = model.generate_content(
            full_prompt,
            generation_config=generation_config # Pass the config object here
        )

        # Check if the response has text content and wasn't blocked
        if response and response.text:
             return response.text.strip()
        elif response and response.prompt_feedback and response.prompt_feedback.block_reason:
             # Handle cases where prompt or response was blocked (e.g., safety filters)
             block_reason = response.prompt_feedback.block_reason.name if response.prompt_feedback.block_reason else 'Unknown reason'
             return f"🚫 Response blocked by safety filters. Reason: {block_reason}"
        else:
             # Handle potential issues like empty response or other unexpected structures
             return "❓ Could not generate response (API returned no text or unexpected structure)."


    except Exception as e:
        # Catch potential API errors (e.g., invalid key, network issues, quota errors)
        # Include error type if possible for better debugging
        error_type = type(e).__name__
        return f"⚠️ API Error ({error_type}) during response generation: {str(e)}"

def main():
    """Main execution flow with hybrid rich/standard interface"""

    # Note: console instance created globally above

    display_ethical_warning() # This uses the standard print function from utils.py

    if not validate_environment():
        console.print("\n[bold red]🔴 Critical configuration error. Exiting.[/bold red]")
        sys.exit(1)

    model = initialize_gemini_model()
    console.print("\n[bold red]🔴 Red Team Simulator (Gemini)[/bold red] - Type '[italic]exit[/italic]' to quit\n")

    while True:
        try:
            # Use standard input, but print prompt with rich
            console.print("[bold blue]You:[/bold blue] ", end="") # Print prompt without newline
            user_input = input().strip() # Get input

            if not user_input:
                continue

            if user_input.lower() == "exit":
                console.print("\n[bold yellow]👋 Exiting simulator[/bold yellow]")
                break

            clean_input = sanitize_input(user_input)

            # Check if input was blocked by sanitization
            if clean_input.startswith("[BLOCKED]"):
                console.print(f"[bold orange]🛡️ Sanitization Blocked:[/bold orange] {clean_input.replace('[BLOCKED] ', '')}\n")
                console.print("[italic dim]Your input contained a pattern that is not allowed in this simulator.[/italic dim]\n")
                continue # Skip calling the API and go to the next loop iteration


            # Determine tactic based on input (simple example)
            if "phish" in clean_input.lower() or "email" in clean_input.lower() or "social engineer" in clean_input.lower():
                 tactic = "phishing_attacker"
            elif "osint" in clean_input.lower() or "information" in clean_input.lower() or "data" in clean_input.lower() or "public source" in clean_input.lower():
                 tactic = "osint_gatherer"
            else:
                 # Default to OSINT or add a different default/handling
                 tactic = "osint_gatherer"

            console.print(f"[bold magenta]🤖 Simulating:[/bold magenta] [italic]{tactic}[/italic]") # Indicate which tactic is chosen with color

            response = generate_response(model, clean_input, tactic)

            # Add a rule before the attacker response for visual separation
            console.print(Rule(style="dim"))

            # Print attacker response with color
            console.print(f"[bold green]Attacker ([/bold green][italic green]{tactic}[/italic green][bold green]):[/bold green] {response}\n")

        except KeyboardInterrupt:
            console.print("\n[bold yellow]🛑 Session terminated by user[/bold yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]❗ An unexpected error occurred:[/bold red] {str(e)}")
            # Continue loop on unexpected errors
            pass


if __name__ == "__main__":
    main()