import os


def generate_pdf_viewer_html(target: str) -> str:
    sb: list[str] = [
        '<div class="preview__wrapper">',
        '<div class="preview__track">',
        '<div class="preview__list">',
    ]

    page_count = __pdf_page_count(target)

    def pad_number(num: int, total: int) -> str: # pads with leading zeros based on max
        total_digits = len(str(total))
        return str(num).zfill(total_digits)
    
    for i in range(1, page_count + 1):
        sb.extend((
            '<div class="preview__item">',
            f'<img class="preview__image on-glb" src="./{target}~preview/{target}_preview-{pad_number(i, page_count)}.png" ',
            f'alt="Page {i} of {target}">',
            f'<div class="preview__caption">Page {i} of {page_count}</div>',
            '</div>',
        ))

    sb.append('</div></div></div>')

    return "".join(sb)

def __pdf_page_count(target: str) -> int:
    return len([f for f in os.listdir(f"./site/docs/downloads/details/{target}~preview") if f.endswith(".png")])