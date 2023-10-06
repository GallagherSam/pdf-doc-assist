import PyPDF2


def load_pdf(file_path):
    reader = PyPDF2.PdfReader(file_path)
    return reader


def read_page(pdf, page_num):
    return pdf.pages[page_num - 1].extract_text().replace("\n", "")


def get_title(pdf, pdf_file_path):
    meta = pdf.metadata
    if meta.title is not None:
        return meta.title
    else:
        if '/' in pdf_file_path:
            return pdf_file_path.split('/')[-1]
        else:
            return pdf_file_path
