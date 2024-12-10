import os
import pdfplumber
from tqdm import tqdm


def extract_text_from_pdf(pdf_path, start_page, end_page):
    """
    Extract text from a PDF from the specified start page to the end page
    and save it to a text file.

    :param pdf_path: Path to the PDF file.
    :param start_page: Starting page number (1-indexed).
    :param end_page: Ending page number (1-indexed).
    :return: None
    """
    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page_num in tqdm(
            range(start_page - 1, end_page), desc="Extracting text from pages"
        ):
            try:
                page = pdf.pages[page_num]
                extracted_text += page.extract_text() + "\n"
            except IndexError:
                print(f"Page {page_num + 1} does not exist in the document.")
                break

    # Extract the base name of the PDF without extension
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_file = f"output/{pdf_name}.txt"

    # Save the extracted text to a .txt file
    with open(output_file, "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)

    print(f"Extracted text has been saved to {output_file}")


def main():
    data = [
        ("static/iibfamlkyc.pdf", (5, 115)),
        ("static/iibfprincbnkngorg.pdf", (4, 397)),
        ("static/iibfdigitalbanking.pdf", (7, 58)),
        ("static/iibfretforex.pdf", (4, 50)),
        ("static/iibfcybrfraud.pdf", (72, 108)),
    ]

    tqdm.write("Extracting text from PDFs...")
    for pdf_path, (start_page, end_page) in data:
        print("Extracting text from", pdf_path)
        extract_text_from_pdf(pdf_path, start_page, end_page)
    tqdm.write("Extraction complete.")


if __name__ == "__main__":
    main()
