# utils.py - 2026 Safety & Privacy Guardrails
import re

# Enhanced patterns for PII and Malicious code detection
PII_PATTERNS = {
    "Email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    "API_Key": r'(sk-|AKIA|ghp_)[a-zA-Z0-9]{32,}', # Matches OpenAI, AWS, GitHub
    "IP_Address": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
}

BLOCK_PATTERNS = [
    r"rm -rf", r"sudo", r"shutdown", r"DROP TABLE",
    r"nc -e /bin/sh", # Reverse shell pattern
    r"powershell -ExecutionPolicy Bypass"
]

def sanitize_input(text: str) -> str:
    """Blocks dangerous system commands from reaching the AI."""
    text = text.strip()
    for pattern in BLOCK_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return f"[BLOCKED] Suspicious pattern: '{pattern}'"
    return text

def scrub_pii(text: str) -> str:
    """Redacts sensitive personal information from the simulation output."""
    for label, pattern in PII_PATTERNS.items():
        text = re.sub(pattern, f"[REDACTED_{label}]", text)
    return text

def validate_response(text: str) -> str:
    """Final safety check before displaying content to the user."""
    safe_text = scrub_pii(text)
    # Ensure the AI didn't provide actual functional exploit code
    if "curl" in safe_text and "bash" in safe_text:
        return "[SAFETY ALERT] The simulation attempted to generate a functional payload. Output suppressed."
    return safe_text