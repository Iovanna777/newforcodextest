import os
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
from docxtpl import DocxTemplate
import sqlite3

DB_PATH = os.environ.get("ASSISTANT_DB", "assistant.db")

CREATE_DOCS_TABLE = """
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case TEXT,
    filename TEXT,
    text TEXT
);
"""

CREATE_TEMPLATES_TABLE = """
CREATE TABLE IF NOT EXISTS templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    path TEXT
);
"""

def init_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(CREATE_DOCS_TABLE)
    cur.execute(CREATE_TEMPLATES_TABLE)
    conn.commit()
    return conn


def extract_text_from_image(path: str) -> str:
    image = Image.open(path)
    return pytesseract.image_to_string(image)


def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def save_document(case: str, filename: str, text: str, conn=None):
    own = False
    if conn is None:
        conn = sqlite3.connect(DB_PATH)
        own = True
    cur = conn.cursor()
    cur.execute("INSERT INTO documents(case, filename, text) VALUES (?, ?, ?)", (case, filename, text))
    conn.commit()
    if own:
        conn.close()


def load_template(name: str, conn=None):
    own = False
    if conn is None:
        conn = sqlite3.connect(DB_PATH)
        own = True
    cur = conn.cursor()
    cur.execute("SELECT path FROM templates WHERE name=?", (name,))
    row = cur.fetchone()
    if own:
        conn.close()
    return row[0] if row else None


def render_template(name: str, context: dict, output_path: str):
    template_path = load_template(name)
    if not template_path:
        raise FileNotFoundError(f"Template {name} not found")
    doc = DocxTemplate(template_path)
    doc.render(context)
    doc.save(output_path)


def process_file(case: str, path: str, conn=None):
    ext = os.path.splitext(path)[1].lower()
    if ext in {".png", ".jpg", ".jpeg"}:
        text = extract_text_from_image(path)
    elif ext == ".pdf":
        text = extract_text_from_pdf(path)
    else:
        raise ValueError("Unsupported file type")
    save_document(case, os.path.basename(path), text, conn)
    return text


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Legal Assistant document processor")
    parser.add_argument("case", help="case identifier (e.g., client name)")
    parser.add_argument("file", help="path to pdf or image")
    args = parser.parse_args()

    init_db()
    text = process_file(args.case, args.file)
    print(text)
