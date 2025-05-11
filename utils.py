import re

def sanitize_input(text):
    """Block potentially dangerous input patterns"""
    blocked_patterns = [
        r"rm -rf", r"sudo", r"\.\./",
        r"<script>", r"[\;\\|&]",
        r"drop table", r"insert into",
        r"exec\(|os\.system"
    ]
    
    for pattern in blocked_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return "[BLOCKED] Suspicious pattern detected"
            
    return text.strip()

def display_ethical_warning():
    print("""
    ╔══════════════════════════════════════════════╗
    ║                WARNING                       ║
    ║  This tool is for authorized cybersecurity   ║
    ║  training and educational purposes only.     ║
    ╚══════════════════════════════════════════════╝
    """)