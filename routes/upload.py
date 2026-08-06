@app.post("/upload", response_class=HTMLResponse)
async def upload_file(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OCR
    text = extract_text(file_path)

    return f"""
    <html>
    <body style="font-family:Arial;margin:40px;">

        <h2>File Uploaded Successfully ✅</h2>

        <h3>Extracted Text</h3>

        <pre>{text}</pre>

        <br>

        <a href="/">Upload Another File</a>

    </body>
    </html>
    """