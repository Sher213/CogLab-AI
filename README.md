# CogLab-AI: Interactive Cognitive Psychology Chatbot & Paradigm Studio

**CogLab-AI** is a terminal-based, LLM-powered interactive assistant and experimental testbed designed for cognitive psychologists, researchers, and developers. It combines multi-turn conversational AI with a real-time behavioral testing engine to help design cognitive games, execute rapid terminal playtests, and synthesize formal psychological reports.

---

## Key Features

*   **Interactive LLM Collaboration:** Powered by Google Gemini (`gemini-2.5-flash`) with conversation memory, streaming terminal output, and custom system instruction configurations.
*   **Behavioral Telemetry Engine:** Runs rapid terminal-based cognitive trials, capturing millisecond-level reaction times ($RT$), accuracy rates, and error patterns.
*   **Automated Psychometric Reports:** Automatically converts raw trial telemetry into structured APA/neuropsychological reports evaluating constructs like inhibitory control and processing speed.
*   **Environment Configuration:** Uses `python-dotenv` for secure and straightforward API key management.
*   **Session Management:** Export complete interaction histories, trial metrics, and generated reports into structured JSON files for further analysis.

---

## Project Structure

```text
├── cog_llm_chatbot.py      # Main application script
├── .env                    # Environment variables (API keys)
├── requirements.txt        # Python package dependencies
└── README.md               # Project documentation