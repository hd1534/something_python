import fitz  # PyMuPDF

# from pprint import pprint


def remove_header_footer(pdf_path, output_path):
    doc = fitz.open(pdf_path)

    for page in doc:
        height = page.rect.height

        # https://pymupdf.readthedocs.io/en/latest/page.html#Page.apply_redactions
        page.add_redact_annot(fitz.Rect(0, 0, 1, 1))  # 왼쪽위 1px
        page.add_redact_annot(fitz.Rect(0, height-1, 1, height))  # 왼쪽 아래 1px
        page.apply_redactions(
            # 위 두 redact_annot에 닿은 drawing 지우기
            graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED)

        # blues = [blue for blue in page.get_drawings() if blue['fill'] == (
        #     0.2784309983253479, 0.5764709711074829, 0.9372550249099731)]
        # pprint(blues)

        # for blue in blues:
        #     page.add_redact_annot(blue['rect'])

        # page.apply_redactions(
        #     graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED)  # 텍스트 박스 삭제 적용

    doc.save(output_path)
    doc.close()
    print(f"머릿글과 바닥글의 텍스트 박스가 제거된 PDF가 저장됨: {output_path}")


# 사용 예제
remove_header_footer("input.pdf", "output.pdf")
