import pytesseract
from PIL import Image
from PyPDF2 import PdfReader


def extract_text_from_pdf(path: str) -> str:
    """Extracts text from a PDF file."""
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_text_from_image(path: str) -> str:
    """Extract text from an image using Tesseract OCR."""
    img = Image.open(path)
    return pytesseract.image_to_string(img, lang="rus+eng")
