from services.image_redactor import redact_image

sensitive = [
    "Raman",
    "9876543210"
]

redact_image(
    "test_images/image.png",
    sensitive,
    "outputs/redacted.png"
)

print("Image redacted successfully!")