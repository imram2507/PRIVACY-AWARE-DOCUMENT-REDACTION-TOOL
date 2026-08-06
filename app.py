import os
import shutil

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from services.summary import create_summary
from services.ocr import extract_text
from services.pdf_ocr import extract_text_from_pdf
from services.pii_detector import detect_pii
from services.redactor import redact_text
from services.image_redactor import redact_image
from services.pdf_redactor import redact_pdf

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/upload", response_class=HTMLResponse)
async def upload_file(file: UploadFile = File(...)):

    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OCR
    if file.filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text(file_path)

    # Detect PII
    detected = detect_pii(text)

    # Redact Text
    redacted = redact_text(text, detected)
    # Create Summary
    summary = create_summary(detected)
    download_section = ""

    # PDF Redaction
    if file.filename.lower().endswith(".pdf"):

        output_pdf = os.path.join(
            OUTPUT_FOLDER,
            "redacted_" + file.filename
        )

        redact_pdf(
            file_path,
            detected,
            output_pdf
        )

        download_section = f"""
        <hr>
        <h2>Download Redacted PDF</h2>

        <a href="/outputs/redacted_{file.filename}" target="_blank">
            Download Redacted PDF
        </a>
        """

    # Image Redaction
    else:

        output_image = os.path.join(
            OUTPUT_FOLDER,
            "redacted_" + file.filename
        )

        redact_image(
            file_path,
            detected,
            output_image
        )

        download_section = f"""
        <hr>
        <h2>Download Redacted Image</h2>

        <a href="/outputs/redacted_{file.filename}" target="_blank">
            Download Redacted Image
        </a>
        """

    detected_html = "<br>".join(detected)

    if detected_html == "":
        detected_html = "No PII Found"

    return f"""
<!DOCTYPE html>
<html lang="en" data-bs-theme="light">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Results - ShieldRedact</title>

<!-- Bootstrap 5 CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Bootstrap Icons -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<!-- Custom Application Stylesheet -->
<link rel="stylesheet" href="/static/style.css">

</head>

<body class="bg-body-tertiary">

<!-- Navbar -->
<nav class="navbar app-navbar mb-4">
  <div class="container d-flex align-items-center justify-content-between">
    <a class="navbar-brand d-flex align-items-center gap-2" href="/">
      <div class="brand-logo-icon">
        <i class="bi bi-shield-lock-fill"></i>
      </div>
      <span class="brand-title">ShieldRedact</span>
    </a>
    <div class="d-flex align-items-center gap-2">
      <button class="btn btn-secondary-custom p-2 px-3" id="themeToggleBtn" aria-label="Toggle theme">
        <i class="bi bi-moon-stars-fill" id="themeIcon"></i>
      </button>
      <a href="/" class="btn btn-primary-custom py-2 px-3 text-white text-decoration-none">
        <i class="bi bi-cloud-arrow-up-fill"></i> Upload Another File
      </a>
    </div>
  </div>
</nav>

<div class="container pb-5">

<h1 class="text-center font-heading mb-4">
Privacy-Aware Document Redaction Tool
</h1>

<div class="card shadow-sm border-0 rounded-4 mb-4 overflow-hidden">

<div class="card-header bg-primary text-white py-3 fw-bold fs-5 d-flex align-items-center gap-2">
<i class="bi bi-file-text-fill"></i> Original Extracted Text
</div>

<div class="card-body">

<pre class="text-viewer-box">{text}</pre>

</div>

</div>

<div class="card shadow-sm border-0 rounded-4 mb-4 overflow-hidden">

<div class="card-header bg-success text-white py-3 fw-bold fs-5 d-flex align-items-center gap-2">
<i class="bi bi-table"></i> Detection Summary
</div>

<div class="card-body p-0">

<table class="table table-hover table-striped mb-0 align-middle">

<thead class="table-light">
<tr>
<th class="ps-4">Category</th>
<th class="pe-4 text-end">Count</th>
</tr>
</thead>

<tbody>
<tr>
<td class="ps-4">Names</td>
<td class="pe-4 text-end fw-bold">{summary["Names"]}</td>
</tr>

<tr>
<td class="ps-4">Emails</td>
<td class="pe-4 text-end fw-bold">{summary["Emails"]}</td>
</tr>

<tr>
<td class="ps-4">Phone Numbers</td>
<td class="pe-4 text-end fw-bold">{summary["Phones"]}</td>
</tr>

<tr>
<td class="ps-4">Aadhaar</td>
<td class="pe-4 text-end fw-bold">{summary["Aadhaar"]}</td>
</tr>

<tr>
<td class="ps-4">PAN</td>
<td class="pe-4 text-end fw-bold">{summary["PAN"]}</td>
</tr>

<tr>
<td class="ps-4">Others</td>
<td class="pe-4 text-end fw-bold">{summary["Others"]}</td>
</tr>
</tbody>

</table>

</div>

</div>

<div class="card shadow-sm border-0 rounded-4 mb-4 overflow-hidden">

<div class="card-header bg-warning py-3 fw-bold fs-5 d-flex align-items-center gap-2 text-dark">
<i class="bi bi-exclamation-triangle-fill"></i> Detected PII
</div>

<div class="card-body">

<p class="mb-0 fs-6">{detected_html}</p>

</div>

</div>

<div class="card shadow-sm border-0 rounded-4 mb-4 overflow-hidden">

<div class="card-header bg-danger text-white py-3 fw-bold fs-5 d-flex align-items-center gap-2">
<i class="bi bi-shield-shaded"></i> Redacted Text
</div>

<div class="card-body">

<pre class="text-viewer-box">{redacted}</pre>

</div>

</div>

<div class="download-section-card mb-4">

<div class="text-center">

{download_section}

</div>

</div>

<div class="text-center mt-4">

<a href="/" class="btn btn-primary-custom btn-lg">
<i class="bi bi-cloud-arrow-up-fill me-2"></i> Upload Another File
</a>

</div>

</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script src="/static/script.js"></script>

</body>

</html>
"""
