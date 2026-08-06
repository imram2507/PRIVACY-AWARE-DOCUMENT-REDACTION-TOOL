import re

def create_summary(detected):

    summary = {
        "Names": 0,
        "Emails": 0,
        "Phones": 0,
        "Aadhaar": 0,
        "PAN": 0,
        "Others": 0
    }

    for item in detected:

        if "@" in item:
            summary["Emails"] += 1

        elif re.fullmatch(r"\d{10}", item):
            summary["Phones"] += 1

        elif re.fullmatch(r"\d{4}\s?\d{4}\s?\d{4}", item):
            summary["Aadhaar"] += 1

        elif re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", item):
            summary["PAN"] += 1

        elif item.replace(" ", "").isalpha():
            summary["Names"] += 1

        else:
            summary["Others"] += 1

    return summary