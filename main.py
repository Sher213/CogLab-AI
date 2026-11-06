#!/usr/bin/env python3
"""
Interactive LLM Cognitive Psychology Chatbot & Game Designer Engine
Powered by Google GenAI (Gemini) with standard chatbot features:
- dotenv integration for key loading
- Multi-turn context memory
- Streaming text output
- Slash commands (/help, /reset, /config, /export, /play, /report)
- Automated trial data capture & formal report generation
"""

import os
import sys
import time
import json
import random
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Validate API Key loaded via dotenv
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment or .env file.")
    print("Ensure a .env file exists with GEMINI_API_KEY='your_api_key'.")
    sys.exit(1)

client = genai.Client()

DEFAULT_SYSTEM_PROMPT = """
You are CogLab-AI, an expert Cognitive Psychologist, Experimental Design Scientist, and Psychometrician.
Your goal is to converse with the user, help them design terminal-playable cognitive psychology games, 
and analyze behavioral performance data to generate formal psychological reports.

Keep conversational responses analytical, structured, and engaging.
"""

class CognitiveLLMChatbot:
    def __init__(self):
        self.model_name = "gemini-2.5-flash"
        self.temperature = 0.7
        self.system_prompt = DEFAULT_SYSTEM_PROMPT
        self.chat = None
        self.session_data = {
            "timestamp": datetime.now().isoformat(),
            "chat_history": [],
            "trial_telemetry": [],
            "report": ""
        }
        self.init_chat_session()

    def init_chat_session(self):
        """Initializes or resets the Gemini chat session with current configurations."""
        self.chat = client.chats.create(
            model=self.model_name,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=self.temperature,
            )
        )

    def stream_response(self, user_text):
        """Sends user text to the LLM and streams the response to the terminal."""
        print("\n[CogLab-AI]: ", end="", flush=True)
        try:
            response_stream = self.chat.send_message_stream(user_text)
            full_response = ""
            for chunk in response_stream:
                print(chunk.text, end="", flush=True)
                full_response += chunk.text
            print()
            
            # Save history to session state
            self.session_data["chat_history"].append({"role": "user", "text": user_text})
            self.session_data["chat_history"].append({"role": "assistant", "text": full_response})
            return full_response
        except Exception as e:
            print(f"\n[Error generating response]: {e}")
            return ""

    def display_help(self):
        print("\n" + "=" * 55)
        print("                AVAILABLE COMMANDS               ")
        print("=" * 55)
        print("  /play    - Launch an interactive 5-trial playtest run")
        print("  /report  - Generate a Cognitive Psychology Report from playtest")
        print("  /config  - View/adjust LLM parameters (Temperature, System Prompt)")
        print("  /reset   - Clear chat history and restart session memory")
        print("  /export  - Export session state (chat, metrics, report) to JSON")
        print("  /help    - Show this help menu")
        print("  /exit    - Exit the chatbot")
        print("=" * 55)

    def run_config_menu(self):
        print(f"\n--- CURRENT CONFIGURATION ---")
        print(f"Model: {self.model_name}")
        print(f"Temperature: {self.temperature}")
        print(f"System Prompt Snippet: {self.system_prompt[:60]}...")
        
        print("\nWhat would you like to update?")
        print("1. Temperature (0.0 - 1.0)")
        print("2. System Prompt Role")
        print("3. Return to chat")
        
        choice = input("Select option (1-3): ").strip()
        if choice == "1":
            try:
                val = float(input("Enter new temperature (e.g., 0.2 for strict, 0.9 for creative): "))
                if 0.0 <= val <= 1.0:
                    self.temperature = val
                    self.init_chat_session()
                    print(f"Temperature updated to {self.temperature}. Chat session re-initialized.")
                else:
                    print("Out of range.")
            except ValueError:
                print("Invalid number.")
        elif choice == "2":
            new_prompt = input("Enter new system prompt: ").strip()
            if new_prompt:
                self.system_prompt = new_prompt
                self.init_chat_session()
                print("System prompt updated. Chat session re-initialized.")

    def run_playtest(self):
        print("\n--- LAUNCHING COGNITIVE PLAYTEST ENGINE ---")
        print("Rule: Press 'space' + Enter for EVEN numbers (Targets). Press Enter for ODD numbers.")
        input("Press ENTER when ready...")
        
        trials = 5
        metrics = []
        
        for i in range(1, trials + 1):
            val = random.randint(10, 99)
            is_target = (val % 2 == 0)
            
            print(f"\nTrial {i}/{trials} -> Stimulus: [ {val} ]")
            t0 = time.time()
            ans = input("Action: ").strip()
            rt = time.time() - t0
            
            user_acted = len(ans) > 0
            correct = (user_acted == is_target)
            
            metrics.append({
                "trial": i,
                "stimulus": val,
                "is_target": is_target,
                "user_acted": user_acted,
                "correct": correct,
                "reaction_time_sec": round(rt, 3)
            })
            print(f"Result: {'CORRECT' if correct else 'INCORRECT'} | Latency: {rt:.3f}s")
            time.sleep(0.4)
            
        self.session_data["trial_telemetry"] = metrics
        print("\nPlaytest complete! Type '/report' to synthesize an LLM analysis of your results.")

    def generate_report(self):
        if not self.session_data["trial_telemetry"]:
            print("\n[Notice]: No trial data available. Run '/play' first to collect performance data.")
            return

        print("\n--- SYNTHESIZING COGNITIVE PSYCHOLOGY REPORT ---")
        prompt = f"""
        Generate a formal Cognitive Psychology & Behavioral Paradigm Report based on the following playtest telemetry:
        
        Trial Telemetry:
        {json.dumps(self.session_data['trial_telemetry'], indent=2)}
        
        Structure the report as follows:
        1. Paradigm Overview & Cognitive Target
        2. Quantitative Metrics (Mean RT, Accuracy %, Target Discrimination)
        3. Neuropsychological & Behavioral Interpretation (Inhibitory control, processing speed, error patterns)
        4. Experimental Recommendations
        """
        report_text = self.stream_response(prompt)
        self.session_data["report"] = report_text

    def export_session(self):
        filename = f"cog_session_{int(time.time())}.json"
        with open(filename, "w") as f:
            json.dump(self.session_data, f, indent=2)
        print(f"\nSession state successfully exported to '{filename}'.")

    def start(self):
        print("=" * 65)
        print("       LLM COGNITIVE PSYCHOLOGY CHATBOT & PARADIGM STUDIO        ")
        print("=" * 65)
        print("Type your message or use commands like /help, /play, /report, /exit.\n")
        
        # Initial greeting
        self.stream_response("Greet the user and invite them to design a cognitive game or ask a psychology question.")

        while True:
            try:
                user_input = input("\n[You]: ").strip()
                if not user_input:
                    continue
                
                # Command Router
                if user_input.startswith("/"):
                    cmd = user_input.lower().split()[0]
                    if cmd in ["/exit", "/quit"]:
                        print("\nClosing session. Goodbye!")
                        break
                    elif cmd == "/help":
                        self.display_help()
                    elif cmd == "/play":
                        self.run_playtest()
                    elif cmd == "/report":
                        self.generate_report()
                    elif cmd == "/config":
                        self.run_config_menu()
                    elif cmd == "/reset":
                        self.init_chat_session()
                        self.session_data["chat_history"] = []
                        self.session_data["trial_telemetry"] = []
                        print("\nSession memory reset.")
                    elif cmd == "/export":
                        self.export_session()
                    else:
                        print(f"Unknown command '{cmd}'. Type /help for available options.")
                else:
                    self.stream_response(user_input)

            except (KeyboardInterrupt, EOFError):
                print("\nSession interrupted. Exiting.")
                break

if __name__ == "__main__":
    bot = CognitiveLLMChatbot()
    bot.start()