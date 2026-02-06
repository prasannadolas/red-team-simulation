
# Red Team Simulator: LLM-Driven Attack Orchestration Framework

**Red Team Simulator** is a sophisticated research framework designed to model and simulate multi-stage cyberattacks using Large Language Models (LLMs). By grounding AI-generated content in the **MITRE ATT&CK® framework**, this tool provides a controlled environment for defensive gap analysis, educational walkthroughs, and security research.

The system utilizes **Gemini 3 Flash** to simulate the "attacker's mindset," helping security professionals understand the technical and psychological nuances of modern threats without deploying actual malicious payloads.

---

##  Features

* **MITRE ATT&CK Alignment**: Automatically maps simulations to specific Tactic IDs and Techniques, including Reconnaissance (TA0043), Initial Access (TA0001), and Execution (TA0002).
* **Unified Attack Orchestrator**: Features a "Full-Chain" mode that sequences multiple attack phases, passing context from one stage to the next to maintain logical consistency.
* **Dual-Layer Safety Guardrails**:
* **Input Sanitization**: Rejects dangerous system commands and shell patterns.
* **Output Scrubbing**: Automatically redacts PII (Emails, IP Addresses, API Keys) and suppresses functional exploit code.


* **Modular Architecture**: Built with a Flask REST API backend and a Google GenAI integration layer for easy extensibility.

---

##  System Architecture

The project is structured to ensure separation of concerns between AI logic, safety protocols, and the web interface:

| Component | Responsibility |
| --- | --- |
| **`app.py`** | Flask server management and API routing. |
| **`chatbot.py`** | Gemini client initialization and attack chain orchestration. |
| **`config.py`** | MITRE ATT&CK mapping and specialized system prompts. |
| **`utils.py`** | Regex-based PII scrubbing and command blacklisting. |

---


###  Project Structure

```text
RED-TEAM-SIMULATION/
├── __pycache__/                # Python bytecode cache files
├── labs-projects/              # Directory for experimental lab work 
├── research-paper-presentation/# Documentation, slides, and research paper
├── templates/                  # Frontend HTML assets
│   └── index.html              # Main UI for the simulator
├── .env                        # Environment variables (API keys)
├── .gitignore                  # Specifies files to be ignored by Git
├── app.py                      # Flask web server and API routing
├── chatbot.py                  # AI orchestration and Gemini client logic
├── config.py                   # MITRE ATT&CK profiles and system prompts
├── README.md                   # Project documentation and setup guide
├── requirements.txt            # List of Python dependencies 
└── utils.py                    # Safety guardrails, PII scrubbing, and sanitization

```

##  Installation & Setup

### Prerequisites

* Python 3.10+
* Google Gemini API Key

### Steps

1. **Clone the repository**:
```bash
git clone https://github.com/your-username/red-team-simulator.git
cd red-team-simulator

```


2. **Install dependencies**:
```bash
pip install -r requirements.txt

```


3. **Configure Environment**:
Create a `.env` file in the root directory and add your API key:
```env
GEMINI_API_KEY=your_actual_api_key_here

```


4. **Run the Application**:
```bash
python app.py

```


The server will start at `http://localhost:5000`.

---

##  Ethical Use & Safety

This tool is strictly for **educational and research purposes**. It is designed to help defenders identify weaknesses in infrastructure and human processes.

* **No Payload Execution**: The system is programmed to describe techniques rather than provide functional malware.
* **Automated Redaction**: Integrated safety filters ensure that sensitive data is never exposed during a simulation.

---