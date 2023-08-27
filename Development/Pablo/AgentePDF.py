import fitz  # PyMuPDF


def read_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)

    num_pages = pdf_document.page_count
    all_text = ""

    for page_num in range(num_pages):
        page = pdf_document[page_num]
        text = page.get_text()
        all_text += text

    pdf_document.close()
    return all_text


# Replace 'your_pdf_file.pdf' with the actual path to your PDF file
pdf_path = "Clase1IA2023.pdf"
pdf_text = read_pdf(pdf_path)

print(pdf_text)
