import re

# Indian UPI ID pattern

UPI_REGEX = re.compile(r"\b([a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}|upi)\b", re.IGNORECASE)


# Indian phone numbers
PHONE_REGEX = re.compile(r"\b(\+91[-\s]?)?[6-9]\d{9}\b")

# URLs / phishing links
URL_REGEX = re.compile(r"https?://[^\s]+")

# Common scam keywords (India-focused)
SCAM_KEYWORDS = [
    "account blocked",
    "verify immediately",
    "urgent",
    "upi",
    "bank alert",
    "account suspension",
    "kyc",
    "click link",
    "limited time",
    "act now",
    "refund pending",
    "otp",
    "security alert"
]
