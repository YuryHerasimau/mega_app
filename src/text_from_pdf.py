import PyPDF2


def extract(file_path: str) -> str:
    """
    Extract text from a PDF file.

    Args:
    - file_path (str): The path to the PDF file to extract text from.

    Returns:
    - str: The extracted text from the PDF file.
    """

    try:
        with open(file_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = " ".join(page.extract_text() for page in pdf_reader.pages)
        return text
    except PyPDF2._utils.PdfStreamError as ex:
        return f"Error reading PDF: {ex}"
