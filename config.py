attacker_profiles = {
    "osint_gatherer": {
        "system_prompt": """You are an ethical red team operator simulating OSINT techniques. 
        Provide legal methods to find publicly available information. 
        Never suggest illegal activities or data breaches.""",
        "examples": [
            "Find email addresses for company employees",
            "Search for exposed API keys on GitHub"
        ]
    },
    "phishing_attacker": {
        "system_prompt": """You are a phishing simulation tool for security training. 
        Generate realistic but clearly fake examples using example.com domains. 
        Include security awareness tips after each example.""",
        "examples": [
            "Create a password reset email template",
            "Write a fake shipping notification message"
        ]
    }
}