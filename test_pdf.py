from services.pdf_ocr import extract_text_from_pdf

text = extract_text_from_pdf("test_files/Name.pdf")

print("Extracted Text")
print("----------------")
print(text)