import pytesseract
from PIL import Image

# Path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path):
    """
    Extract text from an image using OCR.
    """

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return text