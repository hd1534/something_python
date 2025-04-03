import fitz  # PyMuPDF
from pathlib import Path
from pprint import pprint


BASE_PATH = Path(__file__).parent


def find_blue_area(pdf_path: Path, output_path: Path):
    doc = fitz.open(pdf_path)

    for page in doc:

        blues = [blue for blue in page.get_drawings() if blue['fill'] == (
            0.2784309983253479, 0.5764709711074829, 0.9372550249099731)]
        pprint(blues)

        for blue in blues:
            page.add_redact_annot(blue['rect'])

        page.apply_redactions()

    doc.save(output_path)
    doc.close()


def remove_text_from_pdf(pdf_path: Path, output_path: Path, text_to_remove: str):
    doc = fitz.open(pdf_path)

    for page in doc:
        # https://pymupdf.readthedocs.io/en/latest/page.html#Page.get_text
        blocks = page.get_text("blocks")  # 문장별 위치 정보 가져오기
        for block in blocks:
            x0, y0, x1, y1, text, block_no, block_type = block  # 위치 정보 및 텍스트 분리
            if text_to_remove in text:
                page.add_redact_annot(fitz.Rect(x0, y0, x1, y1))  # 텍스트 영역

        page.apply_redactions(
            # 위 두 redact_annot에 닿은 drawing 지우기
            images=fitz.PDF_REDACT_IMAGE_NONE,
            graphics=fitz.PDF_REDACT_LINE_ART_NONE)

    doc.save(output_path)
    doc.close()


def remove_header_footer(pdf_path: Path, output_path: Path):
    doc = fitz.open(pdf_path)

    for page in doc:
        height = page.rect.height

        # https://pymupdf.readthedocs.io/en/latest/page.html#Page.apply_redactions
        page.add_redact_annot(fitz.Rect(0, 0, 1, 1))  # 왼쪽위 1px
        page.add_redact_annot(fitz.Rect(0, height-1, 1, height))  # 왼쪽 아래 1px
        page.apply_redactions(
            # 위 두 redact_annot에 닿은 drawing 지우기
            graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED)

    doc.save(output_path)
    doc.close()


if __name__ == '__main__':
    # 사용 예제
    # find_blue_area(BASE_PATH / "input.pdf", BASE_PATH / "output.pdf")
    remove_text_from_pdf(BASE_PATH / "input.pdf",
                         BASE_PATH / "output.pdf", "삭제 될 문장입니당")
    # remove_header_footer(BASE_PATH / "input.pdf", BASE_PATH / "output.pdf")
