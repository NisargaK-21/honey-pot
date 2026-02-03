🛡️ Agentic Honeypot for Scam Detection & Intelligence Extraction
An AI-powered agentic honeypot system that detects scam intent, autonomously engages scammers in multi-turn conversations, extracts actionable intelligence, and reports results to the GUVI evaluation endpoint.

📌 Problem Overview
Online scams such as UPI fraud, phishing, fake bank alerts, and scam offers continuously adapt based on victim responses. Traditional rule-based detection systems fail against such dynamic behavior.

This project implements an agentic honeypot that:
🚨 Detects scam intent in incoming messages
🤖 Activates a human-like AI agent without revealing detection
🔁 Handles multi-turn conversations
🧠 Extracts scam intelligence incrementally
📤 Reports final intelligence via a mandatory callback API

✨ System Capabilities
Scam intent detection with confidence scoring
Autonomous agentic conversation handling
Multi-turn session management
Intelligence extraction:
UPI IDs
Phone numbers
Phishing links
Suspicious keywords
Secure REST API with API key authentication
Mandatory GUVI final result callback support

🏗️ Architecture
Client / GUVI Platform
        │
        ▼
FastAPI REST API
  ├── Auth Middleware
  ├── Scam Detection Service
  ├── Agent Orchestrator
  │     ├── AI Agent (LLM)
  │     └── Intelligence Extractor
  ├── Session Manager
  └── GUVI Callback Service

🔄 API Flow
Incoming message received via REST API
API key validated
Session loaded or created
Scam detection executed
If scam detected → AI agent engaged
Agent replies with human-like response
Intelligence extracted incrementally
Final callback sent to GUVI after engagement completion

🔐 API Authentication
All requests must include:
x-api-key: <YOUR_SECRET_API_KEY>
Content-Type: application/json

📡 API Endpoint
POST /honeypot/message
Processes a single incoming message event.

Request Body
{
  "sessionId": "unique-session-id",
  "message": {
    "sender": "scammer",
    "text": "Your bank account will be blocked today.",
    "timestamp": 1770005528731
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}

Response
{
  "status": "success",
  "reply": "Why will my account be blocked?"
}

📤 Mandatory GUVI Final Callback
Once scam intent is confirmed and engagement is complete, the system must send a final callback.

Endpoint
POST https://hackathon.guvi.in/api/updateHoneyPotFinalResult

Payload
{
  "sessionId": "abc123-session-id",
  "scamDetected": true,
  "totalMessagesExchanged": 18,
  "extractedIntelligence": {
    "bankAccounts": [],
    "upiIds": ["scammer@upi"],
    "phishingLinks": ["http://malicious-link.example"],
    "phoneNumbers": ["+91XXXXXXXXXX"],
    "suspiciousKeywords": ["urgent", "verify now", "account blocked"]
  },
  "agentNotes": "Scammer used urgency tactics and payment redirection"
}


⚠️ This callback is mandatory for evaluation.
If not sent, the solution will not be scored.

📁 Project Structure
honeypot/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── routes/
│   │   └── honeypot.py
│   ├── services/
│   │   ├── scam_detector.py
│   │   ├── agent.py
│   │   ├── intelligence.py
│   │   ├── orchestrator.py
│   │   └── callback.py
│   ├── models/
│   │   └── schemas.py
│   ├── storage/
│   │   └── session_store.py
│   ├── utils/
│   │   ├── auth.py
│   │   └── regex_patterns.py
│   └── prompts/
│       └── agent_prompt.txt
├── tests/
│   └── test_flow.py
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md

⚙️ Environment Configuration

Create a .env file:

API_KEY=your_secret_key
OPENAI_API_KEY=your_openai_key
GUVI_CALLBACK_URL=https://hackathon.guvi.in/api/updateHoneyPotFinalResult

▶️ Running Locally
Install Dependencies
pip install -r requirements.txt

Start Server
uvicorn app.main:app --host 0.0.0.0 --port 8000

🐳 Docker Deployment
Build Image
docker build -t honeypot .

Run Container
docker run -p 8000:8000 --env-file .env honeypot

🧪 Testing
Minimal but sufficient coverage:
Scam detection logic
One complete conversation flow
GUVI callback payload validation

pytest tests/
⚖️ Ethics & Constraints
❌ No impersonation of real individuals
❌ No illegal or harmful instructions
❌ No harassment or abuse
✅ Responsible handling of extracted data

🧾 One-Line Summary
AI-powered agentic honeypot API that detects scams, engages attackers in multi-turn conversations, extracts intelligence, and reports results to the GUVI evaluation endpoint.