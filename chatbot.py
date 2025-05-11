from openai import OpenAI
import os
from dotenv import load_dotenv
from config import attacker_profiles
from utils import sanitize_input, display_ethical_warning

# Initialize OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(prompt, tactic="osint_gatherer"):
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
        return f"⚠️ Error: {str(e)}"

def main():
    display_ethical_warning()
    print("🔴 Red Team Simulator - Type 'exit' to quit\n")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break
            
            clean_input = sanitize_input(user_input)
            tactic = "phishing_attacker" if "phish" in clean_input.lower() else "osint_gatherer"
            
            response = generate_response(clean_input, tactic)
            print(f"\nAttacker: {response}\n")
            
        except KeyboardInterrupt:
            print("\n🛑 Session terminated")
            break

if __name__ == "__main__":
    main()