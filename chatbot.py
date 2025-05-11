import os
import sys
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from config import attacker_profiles
from utils import sanitize_input, display_ethical_warning

def validate_environment():
    """Validate environment configuration with BOM detection"""
    try:
        env_path = find_dotenv(raise_error_if_not_found=True)
        print(f"🔍 Loading .env from: {env_path}")

        # Read with BOM handling
        with open(env_path, 'r', encoding='utf-8-sig') as f:
            content = f.read().strip()
            if not content.startswith("OPENAI_API_KEY="):
                print("❌ Invalid .env format - must start with OPENAI_API_KEY")
                return False

        load_dotenv(env_path, encoding='utf-8-sig')
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key or len(api_key) < 20:
            print("❌ Invalid API key format")
            return False
            
        print("✅ Environment validation successful")
        return True

    except Exception as e:
        print(f"🔥 Error: {str(e)}")
        return False

def initialize_client():
    """Create OpenAI client with proper error handling"""
    try:
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    except Exception as e:
        print(f"🚨 Client initialization failed: {str(e)}")
        sys.exit(1)

def generate_response(client, prompt, tactic):
    """Generate AI response with error handling"""
    try:
        system_msg = attacker_profiles[tactic]["system_prompt"]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

def main():
    """Main execution flow"""
    display_ethical_warning()
    
    if not validate_environment():
        print("\n🔴 Critical configuration error")
        sys.exit(1)
        
    client = initialize_client()
    print("\n🔴 Red Team Simulator - Type 'exit' to quit\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
                
            if user_input.lower() == "exit":
                print("\n👋 Exiting simulator")
                break
                
            clean_input = sanitize_input(user_input)
            tactic = "phishing_attacker" if "phish" in clean_input.lower() else "osint_gatherer"
            
            response = generate_response(client, clean_input, tactic)
            print(f"\nAttacker: {response}\n")
            
        except KeyboardInterrupt:
            print("\n🛑 Session terminated")
            break

if __name__ == "__main__":
    main()