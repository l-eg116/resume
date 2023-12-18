from pathlib import Path

import yaml
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger


def pdf_to_jpg(path_pdf: str, path_jpg: str) -> None:
    """Convert a PDF file to a series of JPEG images.

    Args:
    ----
        path_pdf (str): The path of the PDF file to be converted to JPEG images.
        path_jpg (str): The path and base file name for the JPEG images. If the PDF has
        multiple pages, each page will be saved as a separate image with a numbered
        file name. If the PDF has only one page, the image will be saved with the
        specified file name.

    Returns:
    -------
        None: The function does not return any value, but it saves the
        PDF pages as JPEG images.
    """
    if not path_pdf.endswith(".pdf"):
        msg = "The input file must be a PDF file."
        raise ValueError(msg)
    if not Path.exists(path_pdf):
        msg = "The input file does not exist at the path provided."
        raise FileNotFoundError(msg)

    pages = convert_from_path(path_pdf)

    if len(pages) > 1:
        for i in range(len(pages)):
            pages[i].save(path_jpg + str(i) + ".jpg", "JPEG")
    else:
        pages[0].save(path_jpg + ".jpg", "JPEG")


def merge_pdfs(pdfs: list, new_path: str) -> None:
    """Merge multiple PDF files into a single PDF file.

    Args:
    ----
        pdfs (list): A list of strings representing the paths of the PDF files
        to be merged.
        new_path (str): A string representing the path of the merged PDF file.

    Returns:
    -------
        None. The function does not return any value, but it creates a new
        PDF file by merging the input PDF files.
    """
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(new_path)
    merger.close()


def load_options(yaml_path: str) -> dict:
    """Load options from a YAML file.

    Args:
    ----
        yaml_path (str): The path to the YAML file.

    Returns:
    -------
        dict: The loaded options as a dictionary.

    Raises:
    ------
        FileNotFoundError: If the YAML file does not exist at the path provided.
        ValueError: If the input file is not a YAML file, the YAML file is empty,
        or the 'languages' key is not a non-empty list.
    """
    if not yaml_path.endswith(".yml") and not yaml_path.endswith(".yaml"):
        msg = "The input file must be a YAML file."
        raise ValueError(msg)
    if not Path.exists(yaml_path):
        msg = "The YAML file does not exist at the path provided."
        raise FileNotFoundError(msg)
    with Path.open(yaml_path) as file:
        options = yaml.safe_load(file)
        if options is None:
            msg = "The YAML file is empty."
            raise ValueError(msg)
        if (
            "languages" not in options
            or not isinstance(options["languages"], list)
            or len(options["languages"]) == 0
        ):
            msg = "The 'languages' key must be a non-empty list."
            raise ValueError(msg)
        return options


if __name__ == "__main__":
    pdf_to_jpg("src/resume-fr/resume.pdf", "src/resume-fr/resume")
    pdf_to_jpg("src/resume-en/resume.pdf", "src/resume-en/resume")
    languages = load_options("src/options.yml")["languages"]
    pdfs_to_merge = []
    if "french" in languages:
        pdfs_to_merge.append("src/resume-fr/resume.pdf")
    if "english" in languages:
        pdfs_to_merge.append("src/resume-en/resume.pdf")
    merge_pdfs(pdfs_to_merge, "docs/pdf/resume.pdf")
    print("Done!")
