import fitz  # PyMuPDF
from pathlib import Path
from pprint import pprint


BASE_PATH = Path(__file__).parent


def remove_rect(doc: fitz.Document):
    for page in doc:

        rects = [rect for rect in page.get_drawings() if rect['fill']
                 is not None]
        pprint(rects)

        for rect in rects:
            page.add_redact_annot(rect['rect'])

        # page.apply_redactions()


def remove_drawings(doc: fitz.Document):
    for page in doc:

        drawings = [drawing for drawing in page.get_drawings() if drawing['fill']
                    is None]
        pprint(drawings)

        for draw in drawings:
            page.add_redact_annot(draw['rect'])

        page.apply_redactions(
            graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED)


def remove_images(doc: fitz.Document):
    for page in doc:

        images = page.get_images(full=True)

        for image in images:
            xref, smask, width, height, bpc, colorspace, alt_colorspace, name, filter, referencer = image
            print(name, page.get_image_bbox(image))
            page.add_redact_annot(page.get_image_bbox(image))

        # page.apply_redactions()


def remove_text(doc: fitz.Document, text_to_remove: str):
    for page in doc:
        # https://pymupdf.readthedocs.io/en/latest/page.html#Page.get_text
        blocks = page.get_text("blocks")  # 문장별 위치 정보 가져오기
        print(blocks)
        for block in blocks:
            x0, y0, x1, y1, text, block_no, block_type = block  # 위치 정보 및 텍스트 분리
            if text_to_remove in text:
                page.add_redact_annot(fitz.Rect(x0, y0, x1, y1))  # 텍스트 영역

        page.apply_redactions(
            # 위 두 redact_annot에 닿은 text 지우기
            images=fitz.PDF_REDACT_IMAGE_NONE,
            graphics=fitz.PDF_REDACT_LINE_ART_NONE)


def remove_header_footer(doc: fitz.Document):
    for page in doc:
        height = page.rect.height

        # https://pymupdf.readthedocs.io/en/latest/page.html#Page.apply_redactions
        page.add_redact_annot(fitz.Rect(0, 0, 1, 1))  # 왼쪽위 1px
        page.add_redact_annot(fitz.Rect(0, height-1, 1, height))  # 왼쪽 아래 1px
        page.apply_redactions(
            # 위 두 redact_annot에 닿은 drawing 지우기
            graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED)


if __name__ == '__main__':
    pdf_path = BASE_PATH / "input.pdf"
    output_path = BASE_PATH / "output.pdf"

    doc = fitz.open(pdf_path)

    remove_rect(doc)
    remove_images(doc)
    remove_drawings(doc)
    remove_text(doc, "문장입니당")
    remove_header_footer(doc)

    doc.save(output_path)
    doc.close()
