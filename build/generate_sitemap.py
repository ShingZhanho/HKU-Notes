"""List canonical HTML pages and advertise the sitemap to crawlers."""
from datetime import datetime, timezone
from pathlib import Path
import subprocess
from urllib.parse import quote

from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

from hkbuild.metadata import REPOSITORY, load

NAMESPACE = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('', NAMESPACE)


def get_last_modified_datetime(target_name, repository=None):
    repository = Path(repository or REPOSITORY)
    source = repository / 'src'
    if target_name:
        source /= target_name
    try:
        result = subprocess.run(['git', 'log', '-1', '--format=%ct', '--', str(source)],
                                cwd=repository, text=True, capture_output=True, check=True)
        timestamp = int(result.stdout.strip())
    except (OSError, ValueError, subprocess.CalledProcessError):
        timestamp = max((path.stat().st_mtime for path in source.rglob('*')
                         if path.is_file() and '.build' not in path.parts), default=0)
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat(timespec='seconds')


def generate(targets, paths, output, site_url):
    output = Path(output)
    base = site_url.rstrip('/') + '/'
    urls = {}
    # Canonicals come from the rendered theme, keeping both signals consistent.
    # Download links remain crawlable; the sitemap promotes their HTML details.
    for file in output.rglob('*.html'):
        if file.name == '404.html':
            continue
        soup = BeautifulSoup(file.read_text(encoding='utf-8'), 'html.parser')
        canonical = soup.find('link', rel='canonical')
        robots = soup.find_all('meta', attrs={'name': lambda v: v and v.lower() in ('robots', 'googlebot')})
        if any({'noindex', 'none'} & set(tag.get('content', '').lower().replace(',', ' ').split()) for tag in robots):
            continue
        if not canonical:
            continue
        url = canonical.get('href', '')
        relative = file.relative_to(output).as_posix()
        candidates = {base + quote(relative, safe='/~')}
        if file.name == 'index.html':
            candidates.add(base + quote(relative[:-10], safe='/~'))
        if url in candidates:
            urls[url] = None
    for target in targets:
        metadata = load(paths.metadata(target))
        if metadata['build']['type'] == 'alias':
            continue
        url = base + quote(f'downloads/details/{target}.html', safe='/~')
        if url in urls:
            urls[url] = get_last_modified_datetime(target, paths.repository)
    tree = ET.Element(f'{{{NAMESPACE}}}urlset')
    for url, modified in sorted(urls.items()):
        item = ET.SubElement(tree, f'{{{NAMESPACE}}}url')
        ET.SubElement(item, f'{{{NAMESPACE}}}loc').text = url
        if modified:
            ET.SubElement(item, f'{{{NAMESPACE}}}lastmod').text = modified
    ET.ElementTree(tree).write(output / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    (output / 'sitemap.xml.gz').unlink(missing_ok=True)
    (output / 'robots.txt').write_text(
        f'User-agent: *\nAllow: /\n\nSitemap: {base}sitemap.xml\n', encoding='utf-8')
