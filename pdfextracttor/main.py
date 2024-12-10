from abc import ABC
import re
import os
from typing import Tuple
import pdfplumber as pdfp


class Docs(ABC):
    path: str
    index_pg: Tuple[int, int]

    def __init__(self, path: str, index_pg: Tuple[int, int]) -> None:
        super().__init__()
        self.path = path
        self.index_pg = index_pg


docs = [
    Docs("tmp/KYCMDfull.pdf", (0, 2)),
    Docs("tmp/MDAccesscrtpayments.pdf", (1, 2)),
]

topics = {
    docs[0]: [
        ("INTRODUCTION", 3),
        ("CHAPTER I: PRELIMINARY", 4),
        ("CHAPTER II: General", 15),
        ("CHAPTER III: Customer Acceptance Policy", 19),
        ("CHAPTER IV: Risk Management", 21),
        ("CHAPTER V: Customer Identification Procedure (CIP)", 22),
        ("Part I: CDD Procedure for Individuals", 24),
        ("Part II: CDD Measures for Sole Proprietary Firms", 34),
        ("Part III: CDD Measures for Legal Entities", 35),
        ("Part IV: Identification of Beneficial Owner", 38),
        ("Part V: On-going Due Diligence", 38),
        ("Part VI: Enhanced and Simplified Due Diligence Procedure", 43),
        ("CHAPTER VII: Record Management", 48),
        (
            "CHAPTER VIII: Reporting Requirements to Financial Intelligence Unit - India",
            50,
        ),
        ("CHAPTER IX: Requirements/obligations under International Agreements", 52),
        ("Communications from International Agencies", 52),
        ("CHAPTER X: Other Instructions", 56),
        ("CHAPTER XI: Repeal Provisions", 69),
        ("Annex I", 70),
        ("Annex II", 73),
        ("Annex III", 83),
        ("Annex IV", 93),
        (
            "Appendix: List of Circulars or part thereof repealed with the issuance of Master Direction",
            96,
        ),
    ],
    docs[1]: [
        ("INTRODUCTION", 3),
        ("SECTION I", 3),
        ("SECTION II", 3),
        ("SECTION III", 5),
        ("3.1 Guidelines for Membership to Centralised Payment Systems", 5),
        ("3.2 Guidelines for Membership to Decentralised Payment Systems", 5),
        ("SECTION IV", 6),
        ("4.1 Sub-membership Facility", 6),
        ("4.2 Sub-membership of Centralised Payment Systems", 7),
        ("4.3 Sub-membership of Decentralised Payment Systems", 8),
        ("SECTION V", 8),
        ("5. Review of Membership", 8),
        (
            "Appendix 1 - Covering letter & Application forms (Centralised Payment Systems)",
            9,
        ),
        ("Covering Letter for Membership to Centralised Payment Systems", 9),
        ("Annex I – Application form for Current Account", 13),
        ("Annex II – Application form for SGL and IDL-SGL Account", 15),
        ("Annex III – Application form for NDS-OM and NDS-CALL membership", 21),
        ("Annex IV – Application form for INFINET membership", 32),
        ("Annex V – Application form for RTGS membership", 35),
        ("Annex VI – Application form for NEFT membership", 51),
        (
            "Appendix 2 - Covering letter & Application form (Decentralised Payment Systems)",
            53,
        ),
        ("Covering Letter for Membership to Decentralised Payment Systems", 53),
        ("Annex I – Application form for Current Account", 55),
        ("ANNEX A", 57),
        (
            "List of Circulars repealed, as the contents of the same have been incorporated in the Master Direction",
            57,
        ),
    ],
}


def filter(text, word="Contents"):
    match = re.search(r"" + word + "\n(.*)", text, re.DOTALL)

    # Extract the content
    if match:
        contents_text = match.group(1).strip()
        return contents_text
    else:
        return text


def extract():
    for _, doc in enumerate(docs):
        pdf = pdfp.open(doc.path)
        # print(f"Extracting {doc.path}...")
        cleaned_text = ""

        for j in range(doc.index_pg[0], doc.index_pg[1]):
            index_page = pdf.pages[j]
            extracted_text = index_page.extract_text() + "\n"
            cleaned_text += filter(extracted_text)

        print(cleaned_text)


# extract()


def extract_page(pdf, topics_list, pg, index):
    cleaned_text = ""
    for j in range(pg - 1, topics_list[index + 1][1] - 1):
        index_page = pdf.pages[j]
        extracted_text = index_page.extract_text() + "\n"
        cleaned_text += extracted_text
    return cleaned_text


def extract_topics():
    for doc_num, (doc, topics_list) in enumerate(topics.items(), start=1):
        pdf = pdfp.open(doc.path)
        print(f"Extracting {doc.path}...")

        output_dir = f"tmp/outputs/{doc_num}"
        os.makedirs(output_dir, exist_ok=True)

        for i, (topic, pg) in enumerate(topics_list):
            if not pg:
                continue

            if i == len(topics_list) - 1:
                break

            cleaned_text = extract_page(pdf, topics_list, pg, i)

            if not cleaned_text:
                print(f"no text extracted for {topic} from {doc.path}")
                continue

            safe_topic_name = (
                topic.replace(" ", "_").replace("/", "_").replace(":", "")
            )  # Make file name safe
            output_file_path = os.path.join(output_dir, f"{safe_topic_name}.txt")
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)


# extract_topics()


class Doc(ABC):
    path: str
    start_pg: int
    end_pg: int

    def __init__(self, path: str, start_pg: int, end_pg: int = None) -> None:
        super().__init__()
        self.path = path
        self.start_pg = start_pg
        self.end_pg = end_pg


def extract_contents(pdf, doc: Doc):
    if doc.end_pg == None:
        doc.end_pg = len(pdf.pages)

    cleaned_text = ""
    for j in range(doc.start_pg - 1, doc.end_pg - 1):
        index_page = pdf.pages[j]
        extracted_text = index_page.extract_text() + "\n"
        cleaned_text += extracted_text

    return cleaned_text


def save_contents(doc: Doc, cleaned_text: str):
    output_dir = f"outputs/contents"
    os.makedirs(output_dir, exist_ok=True)

    file_name = doc.path.split("/")[-1].replace(".pdf", "")

    output_file_path = os.path.join(output_dir, f"{file_name}.txt")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print(f"Contents extracted from {doc.path} saved to {output_file_path}")


def main():
    docs = [
        Doc("tmp/KYCMDfull.pdf", 3, 96),
        Doc("tmp/McircBaselIIIcapreg.pdf", 6, 297),
        Doc("tmp/MDAccesscrtpayments.pdf", 3, 57),
        Doc("tmp/MDBBPS.pdf", 1),
        Doc("tmp/MDCapreqOprisk.pdf", 1),
        Doc("tmp/MDcounterfietnotes.pdf", 3, 25),
        Doc("tmp/MDcrdrcardissuance.pdf", 1, 35),
        Doc("tmp/MDCRRSLR.pdf", 1, 84),
        Doc("tmp/MDdigipaysecontrols.pdf", 3),
        Doc("tmp/MDexchngofnotes.pdf", 1),
        Doc("tmp/MDfemaborrlendngnrisres.pdf", 3, 11),
        Doc("tmp/MDfemadepnaccts.pdf", 3, 26),
        Doc("tmp/MDfemaproptrnf.pdf", 2),
        Doc("tmp/MDfemaremitassets.pdf", 2, 6),
        Doc("tmp/MDFinservbybnks.pdf", 1, 19),
        Doc("tmp/MDforexothrremittancesMD.pdf", 1, 30),
        Doc("tmp/MDfraudrisksallbanks.pdf", 3, 18),
        Doc("tmp/MDitGRCassurnc.pdf", 4, 23),
        Doc("tmp/MDlrsguidelines.pdf", 3, 20),
        Doc("tmp/MDmsmelending.pdf", 1, 11),
        Doc("tmp/MDOmbudsman.pdf", 1),
        Doc("tmp/MDonFraudscombnks.pdf", 4, 34),
        Doc("tmp/MDonPSeclendg.pdf", 3, 39),
        Doc("tmp/MDPPIs.pdf", 1),
        Doc("tmp/MDregfrmMicrofinloans.pdf", 1, 18),
        Doc("tmp/RBIcomplguidelinesallbanks.pdf", 1),
        Doc("tmp/RBIMDSuprvreturns.pdf", 4),
        Doc("tmp/RBIMstrcircCustomerService.pdf", 12, 141),
        Doc("tmp/RBInotificKYCupdation.pdf", 1),
    ]

    for doc in docs:
        pdf = pdfp.open(doc.path)
        print(f"Extracting {doc.path}...")

        cleaned_text = extract_contents(pdf, doc)

        save_contents(doc, cleaned_text)


if __name__ == "__main__":
    main()
