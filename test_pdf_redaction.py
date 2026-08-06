from services.pdf_ocr import extract_text_from_pdf
from services.pii_detector import detect_pii
from services.pdf_redactor import redact_pdf

pdf_path = "test_files/Name.pdf"
output_pdf = "outputs/redacted_Name.pdf"

# Step 1: Extract text from the PDF
text = extract_text_from_pdf(pdf_path)

# Step 2: Detect PII
detected = detect_pii(text)

print("Detected PII:")
print(detected)

# Step 3: Create a redacted PDF
redact_pdf(
    pdf_path,
    detected,
    output_pdf
)

print("\nRedacted PDF created successfully!")
print(f"Saved at: {output_pdf}")