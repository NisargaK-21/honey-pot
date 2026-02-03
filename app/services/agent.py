
import os
import requests
from typing import Optional

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_API_URL = os.getenv("LLM_API_URL")

class Agent:
    
    def rule_based_reply(self, message: str, history: list) -> Optional[str]:
        msg = message.lower()

        if len(history) >= 4:
            return "I already shared details earlier. What exactly is pending now?"

        if "blocked" in msg or "suspended" in msg:
            return "Why would my account get blocked?"

        if "upi" in msg:
            return "I’m not very familiar with UPI. Is there another way?"

        if "otp" in msg:
            return "Why do you need an OTP? I usually don’t share that."

        if "link" in msg or "http" in msg:
            return "Is this an official website?"

        if "pay" in msg or "send" in msg:
            return "I’m confused about the payment process. Can you explain?"

        return None  
    
    def llm_reply(self, message: str) -> Optional[str]:
        
        if not LLM_API_KEY or not LLM_API_URL:
            return None

        try:
            response = requests.post(
                LLM_API_URL,
                headers={
                    "Authorization": f"Bearer {LLM_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "prompt": message,
                    "max_tokens": 50
                },
                timeout=5
            )

            if response.status_code != 200:
                return None

            data = response.json()

            
            return data.get("text") or data.get("response")

        except Exception:
            return None

   
    def reply(self, message: str, history: list) -> str:
        
        rule_reply = self.rule_based_reply(message, history)
        if rule_reply:
            return rule_reply

        llm_reply = self.llm_reply(message)
        if llm_reply:
            return llm_reply

        
        return "Can you explain this again?"



_agent_instance = Agent()

def generate_reply(message: str, history: list) -> str:
    return _agent_instance.reply(message, history)
