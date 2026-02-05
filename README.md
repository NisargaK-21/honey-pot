# Agentic Honeypot — Scam Detection & Intelligence Extraction

A small FastAPI service that detects scam intent from incoming messages, engages suspected scammers with autonomous agent conversations, extracts actionable intelligence (UPI IDs, phone numbers, phishing links, keywords), and sends a final evaluation callback to the GUVI endpoint.

## Key Goals (Project Agenda)
- **Detect** suspicious or scammy messages with confidence scoring.
- **Engage** suspected scammers using an AI-driven, human-like agent in multi-turn sessions without exposing detection.
- **Extract** intelligence incrementally during the conversation (payment handles, phone numbers, links, tactics).
- **Report** a validated final payload to the GUVI evaluation callback endpoint.
- **Measure & Test** core flows: detection, full conversation flow, and callback format.

## Features
- Scam intent detection service with configurable thresholds
- Agent orchestrator that manages multi-turn conversations
- Intelligence extraction and incremental aggregation
- Session management and persistence (in-memory / simple store)
- REST API protected by an API key
- Mandatory GUVI final callback support for evaluation

## Architecture Overview

Client / GUVI Platform -> FastAPI REST API

Main components (under `app/`):
- `main.py` — app entrypoint
- `routes/honeypot.py` — incoming message endpoint(s)
- `services/scam_detector.py` — detection logic
- `services/orchestrator.py` — session/agent orchestration
- `services/agent.py` — agent behaviour / LLM calls
- `services/intelligence.py` — extraction & normalization
- `services/callback.py` — GUVI final payload sender
- `storage/sessions_store.py` — session persistence
- `models/intelligence_models.py` & `models/schemas.py` — data models and Pydantic schemas
- `prompts/agent_prompts.txt` — agent prompt templates

## API (summary)

POST /honeypot/message
- Description: Submit an incoming message event. The system validates API key, loads/creates a session, runs scam detection and (if needed) engages the agent.
- Required header: `x-api-key: <YOUR_SECRET_API_KEY>`
- Example request body:

```
{
  "sessionId": "unique-session-id",
  "message": { "sender":"scammer", "text":"...", "timestamp": 1670000000000 },
  "conversationHistory": [],
  "metadata": { "channel":"SMS", "language":"en", "locale":"IN" }
}
```

Example response:

```
{
  "status": "success",
  "reply": "Why will my account be blocked?"
}
```

### GUVI Final Callback
When a session completes (or is marked finished), the service MUST send a final callback to GUVI for scoring:

POST https://hackathon.guvi.in/api/updateHoneyPotFinalResult

Payload example:

```
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
```

This callback is mandatory for evaluation.

## Environment & Configuration
Create a `.env` file (or set environment variables):

- `API_KEY` — server API key for incoming requests
- `OPENAI_API_KEY` — (if using OpenAI or another LLM provider)
- `GUVI_CALLBACK_URL` — `https://hackathon.guvi.in/api/updateHoneyPotFinalResult`

If `app/config.py` exists, it may read these values at startup.

## Installation (local)
1. Create a virtual environment: `python -m venv .venv`
2. Activate it and install dependencies:

```powershell
pip install -r requirements.txt
```

3. Start the server (development):

```powershell
uvicorn app.main:app --reload
```

## Docker
Build the image:

```powershell
docker build -t honeypot .
```

Run the container (using an `.env` file):

```powershell
docker run -p 8000:8000 --env-file .env honeypot
```

## Testing
Run the test suite:

```powershell
pytest tests/
```

Tests focus on:
- Scam detection logic
- One full conversation flow
- GUVI callback payload validation

## Development notes
- Keep prompts in `app/prompts/agent_prompts.txt` and update for different agent behaviours.
- Tune detection thresholds in `services/scam_detector.py`.
- Persist sessions if you need long-running multi-turn conversations across restarts.

## Roadmap & Milestones (suggested)
1. Core detection + single-message API (complete)
2. Basic agent orchestration + single-turn replies
3. Multi-turn conversation support and session persistence
4. Robust intelligence extraction & normalization
5. End-to-end tests and mandatory GUVI callback compliance

## Contributing
Open issues or submit PRs. Keep changes focused and add tests for new behavior.

## License
Specify an appropriate license for your project.

---
If you want, I can:
- run the test suite now
- add a short `.env.example`
- adjust the README to match specific environment variable names read from `app/config.py`
