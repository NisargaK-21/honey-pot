from app.services.scam_detector import ScamDetector

detector = ScamDetector()

def test_detects_upi_scam():
    text = "Your account will be blocked. Share UPI immediately."
    result = detector.detect(text)

    assert result["scamDetected"] is True
    assert result["confidenceScore"] >= 0.5
    assert result["scamType"] == "UPI Fraud"

def test_detects_phishing_link():
    text = "Click this link now https://fakebank.in to verify KYC"
    result = detector.detect(text)

    assert result["scamDetected"] is True
    assert result["scamType"] == "Phishing"

def test_non_scam_message():
    text = "Hey, are we meeting tomorrow?"
    result = detector.detect(text)

    assert result["scamDetected"] is False
