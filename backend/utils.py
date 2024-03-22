import docx
import fitz
from io import BytesIO


def get_text_from_docx(file_content: bytes):
    doc = docx.Document(BytesIO(file_content))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def get_text_from_txt(file_content: bytes) -> str:
    return file_content.decode("utf-8")


def get_text_from_pdf(file_content: bytes) -> str:
    pdf_document = fitz.open(stream=BytesIO(file_content))
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text
