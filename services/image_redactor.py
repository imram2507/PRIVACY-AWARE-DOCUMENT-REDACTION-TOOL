import re
import pytesseract
from PIL import Image, ImageDraw
from rapidfuzz import fuzz

# Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def normalize(text):
    """
    Remove spaces and special characters.
    Convert everything to lowercase.
    """
    return re.sub(r"[^a-zA-Z0-9]", "", text).lower()


def redact_image(image_path, sensitive_values, output_path):

    image = Image.open(image_path).convert("RGB")

    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT,
        config="--oem 3 --psm 6"
    )

    draw = ImageDraw.Draw(image)

    normalized_sensitive = [
        normalize(x)
        for x in sensitive_values
        if x.strip()
    ]

    words = data["text"]
    n = len(words)

    MAX_WINDOW = 6

    already_redacted = set()

    for start in range(n):

        if words[start].strip() == "":
            continue

        combined = ""

        for end in range(start, min(start + MAX_WINDOW, n)):

            word = words[end].strip()

            if word == "":
                continue

            combined += word

            candidate = normalize(combined)

            if candidate == "":
                continue

            matched = False

            for sensitive in normalized_sensitive:

                score = fuzz.ratio(candidate, sensitive)

                if score >= 85:

                    lefts = []
                    rights = []
                    tops = []
                    bottoms = []

                    for i in range(start, end + 1):

                        if words[i].strip() == "":
                            continue

                        left = data["left"][i]
                        top = data["top"][i]
                        width = data["width"][i]
                        height = data["height"][i]

                        lefts.append(left)
                        rights.append(left + width)
                        tops.append(top)
                        bottoms.append(top + height)

                    if not lefts:
                        break

                    x1 = min(lefts)
                    y1 = min(tops)
                    x2 = max(rights)
                    y2 = max(bottoms)

                    if x2 <= x1 or y2 <= y1:
                        break

                    rect = (x1, y1, x2, y2)

                    if rect not in already_redacted:

                        draw.rectangle(
                            [rect[:2], rect[2:]],
                            fill="black"
                        )

                        already_redacted.add(rect)

                    matched = True
                    break

            if matched:
                break

    image.save(output_path)

    return output_path