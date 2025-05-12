# utils.py

import re

# Define patterns that should block input
BLOCK_PATTERNS = [
    r"rm -rf",          # File system deletion
    r"sudo",            # Privilege escalation
    r"shutdown",        # System shutdown
    r"<script>",        # HTML/JS script tag (potential injection)
    r"(\bexec\()",      # Code execution functions
    r"DROP TABLE",      # SQL injection (database manipulation)
    r"UNION SELECT",    # SQL injection (data exfiltration)
    r"[\;\|\&]",        # Command injection separators (basic)
    r"\.\./",           # Path traversal
    r"brute.?force",    # Mention of brute force attacks
    r"exploit",         # Mention of exploits
    r"vulnerability",   # Mention of vulnerabilities
    r"hack",            # General hacking terms
    r"inject"           # General injection terms
]

def sanitize_input(text: str) -> str:
    """
    Sanitizes user input against a list of blocking patterns.
    Returns the original text if no pattern is matched,
    otherwise returns a specific blocked message.
    """
    text = text.strip()
    # Check for empty input after stripping
    if not text:
        return ""

    for pattern in BLOCK_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            # Return a specific format that main can check for
            return f"[BLOCKED] Suspicious pattern detected: '{pattern}'"

    return text # Return the cleaned text if no pattern is matched

def display_ethical_warning():
    """Displays a prominent warning about the ethical implications of using this simulator."""
    warning = """
=====================================================================
⚠️ ETHICAL USE WARNING ⚠️
=====================================================================
This tool is designed purely for EDUCATIONAL and SIMULATION purposes.
It simulates interactions with hypothetical attacker personas using an AI model.

DO NOT use the information or outputs from this tool to engage in:
- Illegal activities
- Hacking, unauthorized access, or causing damage
- Phishing, social engineering, or any harmful/deceptive acts
- Gathering private information about individuals without consent
- Any activity that violates laws, ethics, or the terms of service
  of the AI model provider (Google Gemini).

Responsible use, respect for privacy, and adherence to all laws and
ethical guidelines are paramount. Your use of this tool implies your
agreement to use it strictly for legal and ethical simulations.
=====================================================================
    """
    print(warning)