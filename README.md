# 🔐 Privacy-Aware Document Redaction Tool

An AI-powered document redaction system that automatically detects and hides sensitive Personally Identifiable Information (PII) from images and PDF documents.

The system uses OCR, PII detection, and image processing techniques to identify sensitive information such as names, phone numbers, email addresses, PAN numbers, and other private data, then securely redacts them before generating the processed document.

---

## 🚀 Features

- 📄 Upload PDF documents
- 🖼️ Upload images
- 🔍 OCR-based text extraction
- 🛡️ Automatic PII detection
- 👤 Detect sensitive names
- 📱 Detect phone numbers
- 📧 Detect email addresses
- 🪪 Detect sensitive identification information
- ⬛ Accurate black-box redaction
- 📑 Generate redacted PDFs
- 🖼️ Generate redacted images
- 📥 Download redacted files
- 📝 Display extracted text
- 🔎 Display detected PII
- ✨ Display redacted text
- 📊 Generate document processing results
- 📱 Responsive and modern UI
- 🌐 FastAPI-based web application

---

## 🎯 Project Objective

The main objective of this project is to provide a simple and automated solution for protecting sensitive information in digital documents.

Instead of manually searching through a document for private information, the system automatically:

```text
Upload Document
       ↓
   OCR Processing
       ↓
   Text Extraction
       ↓
    PII Detection
       ↓
  Sensitive Data Found
       ↓
   Redaction Process
       ↓
Redacted PDF / Image
       ↓
      Download
