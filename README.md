# 🔴 Red Team LLM Simulation Chatbot

A command-line chatbot that simulates adversarial behavior using Large Language Models (LLMs). Designed for **cybersecurity education**, this tool mimics attacker personas like **OSINT gatherers** and **phishing attackers** powered by OpenAI's GPT-3.5.

⚠️ For educational and authorized use only. Do not use this for real-world malicious purposes.

---

## 🚀 Features

- 🧠 **LLM-Powered Simulation** using OpenAI GPT-3.5
- 🎭 Dynamic attacker personas (e.g., OSINT gatherer, phishing attacker)
- 🧼 Input sanitization to prevent malicious command injection
- 💡 Configurable prompts and profiles via `config.py`
- 🛠 Extensible design for additional attacker tactics

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/red-team-simulator.git
cd red-team-simulator
pip install -r requirements.txt
```

---

## 🔧 Setup

1. Create a `.env` file in the root directory:
    ```env
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the chatbot:
    ```bash
    python main.py
    ```

---

## 🛡️ Example Use Cases

| User Input                         | Simulated Attacker Response Role     |
|-----------------------------------|--------------------------------------|
| “Find info on John Doe.”          | OSINT Gatherer                       |
| “Craft a phishing email for HR.”  | Phishing Attacker                    |

The chatbot auto-selects the attacker type based on input keywords (`phish`, `email`, etc.).

---

## 📁 Project Structure

```
.
├── main.py              # Entry point for the chatbot
├── config.py            # Attacker profiles and prompts
├── utils.py             # Input sanitization and helpers
├── .env                 # Your OpenAI API key
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 🧪 Requirements

- Python 3.8+
- [OpenAI Python SDK](https://pypi.org/project/openai/)
- `python-dotenv`

`requirements.txt` example:

```
openai
python-dotenv
```

---

## 🧰 Future Plans

- Add more attacker profiles (e.g., malware coder, insider threat)
- Web-based UI with chat history
- Integration with simulation platforms like TryHackMe or Hack The Box

---

## 🙏 Disclaimer

This tool is intended strictly for **ethical hacking**, **cybersecurity training**, and **academic research**. Misuse may violate OpenAI's terms and cybersecurity laws.
## Documentation

You can download the research paper and presentation from the following links:

- [Research Paper](documentation/ResearchPaper.pdf)
- [Presentation](documentation/Presentation.pdf)