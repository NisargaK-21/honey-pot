from app.utils.regex_patterns import (
    UPI_REGEX,
    PHONE_REGEX,
    URL_REGEX,
    SCAM_KEYWORDS
)

class ScamDetector:

    def detect(self, text: str, sender: str = None) -> dict:
        t = text.lower()

        keyword_hits = [kw for kw in SCAM_KEYWORDS if kw in t]

        upi = bool(UPI_REGEX.search(t))
        phone = bool(PHONE_REGEX.search(t))
        url = bool(URL_REGEX.search(t))

        score = 0
        if keyword_hits:
            score += 0.3
        if upi:
            score += 0.4
        if url:
            score += 0.4
        if phone:
            score += 0.2
        if sender and "scammer" in sender.lower():
            score += 1  

        score = min(score, 1)

        return {
            "scamDetected": score >= 0.5,
            "confidenceScore": round(score, 2),
            "scamType": self._classify(t),
            "reasons": keyword_hits
        }

    def _classify(self, text: str):
        if "upi" in text:
            return "upi_phishing"
        if "otp" in text:
            return "otp_scam"
        if "bank" in text:
            return "bank_impersonation"
        if "http" in text:
            return "phishing"
        return "unknown"

_detector = ScamDetector()

def detect_scam(text: str, sender: str = None):
    return _detector.detect(text, sender)
