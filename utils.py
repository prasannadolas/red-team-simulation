import re

def sanitize_input(text):
    """Block malicious patterns in user input"""
    blocked = [
        r"rm -rf", r"sudo", r"\.\./", 
        r"<script>", r"[\;\\|&]"
    ]
    for pattern in blocked:
        if re.search(pattern, text, re.IGNORECASE):
            return "[BLOCKED] Suspicious input detected"
    return text.strip()

def display_ethical_warning():
    print("""
    ⚠️ ETHICAL USE ONLY ⚠️
    This tool is for authorized cybersecurity training.
    Never use these techniques without explicit permission.
    """)