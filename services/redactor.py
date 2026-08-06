def redact_text(text, sensitive_values):

    redacted = text

    for value in sensitive_values:
        redacted = redacted.replace(
            value,
            "█" * len(value)
        )

    return redacted