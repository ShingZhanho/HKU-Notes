import os


def generate_pdf_viewer_html(target: str) -> str:
    sb: list[str] = [
        '<div class="splide__wrapper">',
        '<section aria-label="PDF Preview" class="splide">',
        '<div class="splide__track">',
        '<ul class="splide__list" style="display: flex !important;">',
    ]

    page_count = __pdf_page_count(target)

    def pad_number(num: int, total: int) -> str: # pads with leading zeros based on max
        total_digits = len(str(total))
        return str(num).zfill(total_digits)
    
    for i in range(1, page_count + 1):
        sb.extend((
            '<li class="splide__slide">',
            f'<img class="splide__image on-glb" src="./{target}~preview/{target}_preview-{pad_number(i, page_count)}.png" alt="Page {i} of {target}">',
            f'<div class="splide__caption">Page {i} of {page_count}</div>',
            '</li>',
        ))

    sb.append('<li class="splide__slide splide__slide--pseudo"></li>')

    sb.append('</ul></div></section></div>')

    return "".join(sb)

def __pdf_page_count(target: str) -> int:
    return len([f for f in os.listdir(f"./site/docs/downloads/details/{target}~preview") if f.endswith(".png")])