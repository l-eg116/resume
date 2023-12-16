import os
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger


def pdf_to_jpg(path_pdf: str, path_jpg: str) -> None:
    """
    Converts a PDF file to a series of JPEG images.

    Args:
        path_pdf (str): The path of the PDF file to be converted to JPEG images.
        path_jpg (str): The path and base file name for the JPEG images. If the PDF has multiple pages, each page will be saved as a separate image with a numbered file name. If the PDF has only one page, the image will be saved with the specified file name.

    Returns:
        None: The function does not return any value, but it saves the PDF pages as JPEG images.
    """
    if not path_pdf.endswith(".pdf"):
        raise ValueError("The input file must be a PDF file.")
    if not os.path.exists(path_pdf):
        raise FileNotFoundError("The input file does not exist at the path provided.")

    pages = convert_from_path(path_pdf)

    if len(pages) > 1:
        for i in range(len(pages)):
            pages[i].save(path_jpg + str(i) + ".jpg", "JPEG")
    else:
        pages[0].save(path_jpg + ".jpg", "JPEG")


def merge_pdfs(pdfs: list, new_path: str) -> None:
    """
    Merge multiple PDF files into a single PDF file.

    Args:
        pdfs (list): A list of strings representing the paths of the PDF files to be merged.
        new_path (str): A string representing the path of the merged PDF file.

    Returns:
        None. The function does not return any value, but it creates a new PDF file by merging the input PDF files.
    """
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(new_path)
    merger.close()


if __name__ == "__main__":
    pdf_to_jpg("../resume-fr/resume.pdf", "../resume-fr/resume")
    pdf_to_jpg("../resume-en/resume.pdf", "../resume-en/resume")

    merge_pdfs(
        ["../resume-fr/resume.pdf", "../resume-en/resume.pdf"], "../docs/pdf/resume.pdf"
    )
