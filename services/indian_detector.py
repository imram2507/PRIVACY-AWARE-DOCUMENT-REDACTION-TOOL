import re

text = """
Name : Raman

Aadhaar : 1234 5678 9012

PAN : ABCDE1234F

IFSC : SBIN0001234
"""

aadhaar_pattern = r"\b\d{4}\s\d{4}\s\d{4}\b"
pan_pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
ifsc_pattern = r"\b[A-Z]{4}0[A-Z0-9]{6}\b"

print("Aadhaar Numbers:")
for match in re.finditer(aadhaar_pattern, text):
    print(match.group())

print("\nPAN Numbers:")
for match in re.finditer(pan_pattern, text):
    print(match.group())

print("\nIFSC Codes:")
for match in re.finditer(ifsc_pattern, text):
    print(match.group())