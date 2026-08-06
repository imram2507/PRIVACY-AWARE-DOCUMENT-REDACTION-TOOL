import re
from presidio_analyzer import AnalyzerEngine
from ocr import extract_text

# Create analyzer
analyzer = AnalyzerEngine()

# Read text from image
text = extract_text("test_images/image.png")

print("========== ORIGINAL TEXT ==========\n")
print(text)

# --------------------------
# Collect sensitive values
# --------------------------

sensitive_values = []

# Presidio Detection
results = analyzer.analyze(
    text=text,
    language="en"
)

for result in results:
    value = text[result.start:result.end]

    if value not in sensitive_values:
        sensitive_values.append(value)

# Indian Regex Detection

aadhaar_pattern = r"\b\d{4}\s\d{4}\s\d{4}\b"
pan_pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
ifsc_pattern = r"\b[A-Z]{4}0[A-Z0-9]{6}\b"

patterns = [
    aadhaar_pattern,
    pan_pattern,
    ifsc_pattern
]

for pattern in patterns:

    matches = re.finditer(pattern, text)

    for match in matches:

        value = match.group()

        if value not in sensitive_values:
            sensitive_values.append(value)

print("\n========== DETECTED PII ==========\n")

for item in sensitive_values:
    print(item)

# --------------------------
# Redaction
# --------------------------

redacted_text = text

for value in sensitive_values:

    replacement = "█" * len(value)

    redacted_text = redacted_text.replace(value, replacement)

print("\n========== REDACTED DOCUMENT ==========\n")

print(redacted_text)