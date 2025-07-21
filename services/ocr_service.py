import fitz  # PyMuPDF

def extract_resume_text(file_bytes):
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        return "".join(page.get_text() for page in doc)
