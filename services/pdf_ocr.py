from pdf2image import convert_from_path
import pytesseract
import os

# Update if your installation paths are different
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = r"C:\poppler-26.02.0\Library\bin"

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(
        pdf_path,
        poppler_path=POPPLER_PATH
    )

    text = ""

    for page in pages:

        temp_image = "temp_page.png"

        page.save(temp_image, "PNG")

        text += pytesseract.image_to_string(temp_image)

        os.remove(temp_image)

    return text