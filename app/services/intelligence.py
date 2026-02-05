import re
from app.models.intelligence_models import Intelligence

UPI_REGEX = r"\b[\w.\-]{2,}@[a-zA-Z]{2,}\b"
URL_REGEX = r"https?://[^\s]+"
PHONE_REGEX = r"(?:\+91|0)?[6-9]\d{9}"
BANK_REGEX = r"\b\d{9,18}\b"

KEYWORDS = [
    "urgent",
    "verify",
    "account blocked",
    "suspended",
    "otp",
    "pay",
    "transfer",
    "click link"
]


def extract_intelligence(text: str, intelligence: Intelligence):
    lower = text.lower()

    intelligence.upiIds.extend(
        re.findall(UPI_REGEX, text)
    )

    intelligence.phishingLinks.extend(
        re.findall(URL_REGEX, text)
    )

    phones = re.findall(PHONE_REGEX, text)
    intelligence.phoneNumbers.extend(phones)

    banks = re.findall(BANK_REGEX, text)

    for b in banks:
        if b not in phones:
            intelligence.bankAccounts.append(b)


    for kw in KEYWORDS:
        if kw in lower and kw not in intelligence.suspiciousKeywords:
            intelligence.suspiciousKeywords.append(kw)
def update_agent_notes(intelligence: Intelligence):

    notes = []

    if intelligence.upiIds:
        notes.append("Requested UPI payment")

    if intelligence.phishingLinks:
        notes.append("Shared suspicious links")

    if intelligence.phoneNumbers:
        notes.append("Provided phone number")

    if "urgent" in intelligence.suspiciousKeywords:
        notes.append("Used urgency tactics")

    intelligence.agentNotes = "; ".join(notes)
