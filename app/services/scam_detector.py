from app.utils.regex_patterns import (
    UPI_REGEX,
    PHONE_REGEX,
    URL_REGEX,
    SCAM_KEYWORDS
)

class ScamDetector:
    def detect(self, text: str) -> dict:
        text_lower = text.lower()

        keyword_hits = [kw for kw in SCAM_KEYWORDS if kw in text_lower]

        upi_found = bool(UPI_REGEX.search(text_lower))
        phone_found = bool(PHONE_REGEX.search(text_lower))
        url_found = bool(URL_REGEX.search(text_lower))

        # FIXED scoring logic
        score = 0.0
        if keyword_hits:
            score += 0.4
        if upi_found:
            score += 0.4
        if url_found:
            score += 0.4
        if phone_found:
            score += 0.2

        score = min(score, 1.0)

        scam_detected = score >= 0.5

        return {
            "scamDetected": scam_detected,
            "confidenceScore": round(score, 2),
            "scamType": self._classify_scam(text_lower),
            "reasons": keyword_hits
        }

    def _classify_scam(self, text: str) -> str:
        # ORDER MATTERS — FIXED
        if "http" in text or "link" in text:
            return "Phishing"
        if "upi" in text:
            return "UPI Fraud"
        if "bank" in text or "account" in text:
            return "Bank Impersonation"
        if "otp" in text:
            return "OTP Scam"
        return "Unknown Scam"
    
    # Function wrapper for orchestrator compatibility
_detector_instance = ScamDetector()

def detect_scam(text: str) -> dict:
    return _detector_instance.detect(text)

