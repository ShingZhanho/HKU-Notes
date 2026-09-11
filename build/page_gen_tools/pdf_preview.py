"""Embed converted PDF pages in the final HTML, after Markdown processing."""
from hashlib import sha256
from html import escape
from pathlib import Path
import re
from urllib.parse import quote

from bs4 import BeautifulSoup


def generate_pdf_viewer_html(target: str, docs) -> str:
    # Zensical must not parse or escape the converter's nested markup as Markdown.
    return f'<div data-html-preview="{escape(target, quote=True)}"></div>'


def render_preview(target, preview_dir):
    soup = BeautifulSoup((preview_dir / 'document.html').read_text(), 'html.parser')
    pages = soup.select('#page-container .pf')
    if not pages:
        raise ValueError(f'Missing HTML preview pages for {target}; run make preview')
    prefix = quote(target + '~preview', safe='~') + '/'
    css = '\n'.join(tag.get_text() for tag in soup.find_all('style'))
    for link in soup.select('link[rel="stylesheet"]'):
        path = (preview_dir / link['href']).resolve()
        if not path.is_relative_to(preview_dir.resolve()):
            raise ValueError('Preview stylesheet escapes its asset directory')
        css += '\n' + path.read_text()
    def asset(url):
        if url.startswith('data:') or url.startswith('#'):
            return url
        if ':' in url or url.startswith('/') or '..' in Path(url).parts:
            raise ValueError(f'Unexpected preview asset URL: {url}')
        return prefix + url
    css = re.sub(r'url\([\'\"]?([^\)\'\"]+)[\'\"]?\)', lambda m: 'url("' + asset(m[1]) + '")', css)
    # Chromium does not consistently load @font-face defined only inside shadow
    # styles. Expose only uniquely named fonts; all element rules remain isolated.
    font_prefix = 'hku' + sha256(target.encode()).hexdigest()[:12] + '_'
    css = re.sub(r'(font-family\s*:\s*)(ff[0-9a-f]+)\b', lambda m: m[1] + font_prefix + m[2], css)
    fonts = '\n'.join(re.findall(r'@font-face\s*\{[^}]*\}', css))
    css = re.sub(r'@font-face\s*\{[^}]*\}', '', css)
    frames = []
    for number, page in enumerate(pages, 1):
        for tag in page.select('[src]'):
            tag['src'] = asset(tag['src'])
            if tag.name == 'img' and not tag.has_attr('alt'):
                tag['alt'] = ''  # PDF backgrounds are not semantic diagram descriptions.
        for link in page.select('a[href]'):
            href = link['href'].strip()
            if ':' in href and href.split(':', 1)[0].lower() not in ('http', 'https', 'mailto'):
                del link['href']
        page['role'] = 'group'
        page['aria-label'] = f'Page {number} of {len(pages)}'
        frames.append(f'<section class="page-frame" data-page="{number}">{page}<p class="page-caption">Page {number} of {len(pages)}</p></section>')
    style = Path(__file__).resolve().parents[2] / 'site/docs/stylesheets/preview.css'
    options = ''.join(f'<option value="{n}">{n}</option>' for n in range(1, len(pages) + 1))
    return (f'<style data-preview-fonts>{fonts}</style><hku-pdf-preview aria-label="{escape(target)} document preview">'
            '<template shadowrootmode="open">'
            f'<style>{css}\n{style.read_text()}</style>'
            '<div class="reader"><div class="toolbar" hidden>'
            f'<label>Page <select aria-label="Go to page">{options}</select> / {len(pages)}</label>'
            '<div class="zoom-controls"><button type="button" data-action="out" aria-label="Zoom out">−</button>'
            '<button type="button" data-action="fit">Fit width</button>'
            '<button type="button" data-action="in" aria-label="Zoom in">+</button></div></div>'
            '<div class="pages">' + ''.join(frames) + '</div></div></template></hku-pdf-preview>')


def embed_previews(output):
    for file in (output / 'downloads/details').glob('*.html'):
        text = file.read_text()
        def replace(match):
            target = match[1]
            if not re.fullmatch(r'[A-Za-z0-9_.-]+', target):
                raise ValueError(f'Invalid preview target: {target}')
            return render_preview(target, file.parent / (target + '~preview'))
        text = re.sub(r'<div data-html-preview="([^"]+)"></div>', replace, text)
        file.write_text(text, encoding='utf-8')
    # Raw converter HTML is a build input, not a second public/indexable page.
    for file in (output / 'downloads/details').glob('*~preview/document.html'):
        file.unlink()
