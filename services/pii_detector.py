import re
from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()

ALLOWED_ENTITIES = [
    "PERSON",
    "PHONE_NUMBER",
    "EMAIL_ADDRESS",
    "CREDIT_CARD",
    "URL",
    "IP_ADDRESS"
]

def detect_pii(text):
    sensitive_values = []

    # Presidio Detection
    results = analyzer.analyze(text=text, language="en")

    for result in results:
        if result.entity_type in ALLOWED_ENTITIES and result.score >= 0.5:
            value = text[result.start:result.end]
            if value not in sensitive_values:
                sensitive_values.append(value)

    # Indian Patterns
    patterns = [
        r"\b\d{4}\s\d{4}\s\d{4}\b",      # Aadhaar
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",    # PAN
        r"\b[A-Z]{4}0[A-Z0-9]{6}\b"      # IFSC
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, text):
            if match.group() not in sensitive_values:
                sensitive_values.append(match.group())

    return sensitive_values