# Legal Assistant Prototype

This repository contains a minimal prototype for a local document management assistant for legal professionals. The application is built using Python and Flask. It can extract text from PDF files or images (screenshots/photographs), store the data in a SQLite database and generate new documents from templates.

## Features

- **OCR and PDF parsing** using `pytesseract` and `PyPDF2`.
- **Document database** stored in SQLite.
- **Template rendering** using `docxtpl` (Microsoft Word `.docx` templates).
- **Simple CLI** via `assistant.py` to process uploaded files.
- **Flask Admin interface** (see `app.py`) for managing cases, documents and templates.

This is a starting point and does not include a full conversational interface or advanced access controls. It can be extended to run entirely offline on a local server.

## Setup

1. Install dependencies (ideally inside a virtual environment):

   ```bash
   pip install -r requirements.txt
   ```

2. Initialize the database and start the Flask development server:

   ```bash
   python app.py
   ```

3. Upload PDF or image files through the admin panel or process them via:

   ```bash
   python assistant.py "Client Name" path/to/file.pdf
   ```

## Notes

- `pytesseract` requires the Tesseract OCR engine installed on the system.
- This project is a minimal demonstration and should be expanded with proper authentication, error handling and a conversational interface for production use.
