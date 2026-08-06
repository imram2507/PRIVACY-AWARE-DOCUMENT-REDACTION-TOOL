from presidio_analyzer import AnalyzerEngine
from ocr import extract_text

# Create analyzer
analyzer = AnalyzerEngine()

# Read text from image
text = extract_text("test_images/image.png")

print("Extracted Text")
print("----------------")
print(text)

print("\nDetected Sensitive Information")
print("--------------------------------")

results = analyzer.analyze(
    text=text,
    language="en"
)

for result in results:

    detected = text[result.start:result.end]

    print(f"Entity : {result.entity_type}")
    print(f"Value  : {detected}")
    print(f"Score  : {result.score:.2f}")

    print("-----------------------------")