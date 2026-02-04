from app.services.intelligence import extract_intelligence, update_agent_notes
from app.models.intelligence_models import Intelligence


def test_upi_and_url_extraction():
    intel = Intelligence()

    text = "Pay me at fraudster@upi and visit http://evil.com"

    extract_intelligence(text, intel)

    assert "fraudster@upi" in intel.upiIds
    assert "http://evil.com" in intel.phishingLinks


def test_phone_and_keywords():
    intel = Intelligence()

    text = "URGENT! Call +919876543210 to verify account"

    extract_intelligence(text, intel)

    assert "+919876543210" in intel.phoneNumbers
    assert "urgent" in intel.suspiciousKeywords


def test_agent_notes_generation():
    intel = Intelligence()

    intel.upiIds.append("abc@upi")
    intel.suspiciousKeywords.append("urgent")

    update_agent_notes(intel)

    assert "UPI" in intel.agentNotes or "upi" in intel.agentNotes.lower()
