from pdf2image import convert_from_path
from PIL import Image
import os

from services.image_redactor import redact_image

# Poppler path
POPPLER_PATH = r"C:\poppler-26.02.0\Library\bin"


def redact_pdf(pdf_path, sensitive_values, output_pdf):

    # Convert PDF pages into images
    pages = convert_from_path(
        pdf_path,
        dpi=400,
        poppler_path=POPPLER_PATH
    )

    temp_images = []

    os.makedirs("temp_pages", exist_ok=True)

    # Process each page
    for i, page in enumerate(pages):

        page_path = f"temp_pages/page_{i}.png"

        page.save(page_path)

        redacted_path = f"temp_pages/redacted_{i}.png"

        # Redact the image page
        redact_image(
            page_path,
            sensitive_values,
            redacted_path
        )

        temp_images.append(
            Image.open(redacted_path).convert("RGB")
        )

    # Save all pages into one PDF
    temp_images[0].save(
        output_pdf,
        save_all=True,
        append_images=temp_images[1:]
    )

    return output_pdf