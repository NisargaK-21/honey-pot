from app.utils.regex_patterns import (
    UPI_REGEX,
    PHONE_REGEX,
    URL_REGEX,
    SCAM_KEYWORDS
)

class ScamDetector:

    def detect(self, text: str) -> dict:
        lower = text.lower()

        keyword_hits = [kw for kw in SCAM_KEYWORDS if kw in lower]

        upi = bool(UPI_REGEX.search(lower))
        phone = bool(PHONE_REGEX.search(lower))
        url = bool(URL_REGEX.search(lower))

        score = 0.0

        if keyword_hits:
            score += 0.3
        if upi:
            score += 0.4
        if url:
            score += 0.4
        if phone:
            score += 0.2

        score = min(score, 1.0)

        scam_detected = score >= 0.5

        scam_type = self._classify(lower)

        analysis = self._build_analysis(
            keyword_hits,
            upi,
            url,
            phone
        )

        action = self._recommended_action(scam_type)

        return {
            "scamDetected": scam_detected,
            "confidence": round(score, 2),
            "scam_type": scam_type,
            "analysis": analysis,
            "recommended_action": action
        }

    def _classify(self, text: str) -> str:

        if "upi" in text:
            return "upi_phishing"

        if "otp" in text:
            return "otp_scam"

        if "bank" in text or "account" in text:
            return "bank_impersonation"

        if "http" in text or "link" in text:
            return "phishing_link"

        return "unknown"

    def _build_analysis(self, keywords, upi, url, phone):

        reasons = []

        if keywords:
            reasons.append("urgent or payment related language")

        if upi:
            reasons.append("UPI handle detected")

        if url:
            reasons.append("suspicious link found")

        if phone:
            reasons.append("phone number present")

        return ", ".join(reasons) if reasons else "No strong indicators found"

    def _recommended_action(self, scam_type):

        mapping = {
            "upi_phishing": "Block sender and report to bank",
            "otp_scam": "Never share OTP and contact bank support",
            "bank_impersonation": "Verify with official bank channel",
            "phishing_link": "Do not click the link and report it",
            "unknown": "Be cautious and avoid sharing sensitive info"
        }

        return mapping.get(scam_type, "Stay alert")


_detector = ScamDetector()

def detect_scam(text: str):
    return _detector.detect(text)
