"""Explicit post-deployment IndexNow notifications (not Google Indexing API)."""
import argparse
from pathlib import Path
import re
import sys
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

import requests


def get_urls_to_index(sitemap: Path) -> list[str]:
    tree = ET.parse(sitemap)
    return list(dict.fromkeys(element.text for element in tree.findall('./{*}url/{*}loc')
                              if element.text))


def submit_to_indexnow(urls: list[str], api_key: str, site_url: str) -> None:
    base = site_url.rstrip('/') + '/'
    if not re.fullmatch(r'[a-zA-Z0-9-]{8,128}', api_key):
        raise ValueError('Invalid IndexNow key')
    if urlparse(base).scheme not in ('http', 'https') or not urlparse(base).netloc:
        raise ValueError('Site URL must be an absolute HTTP(S) URL')
    if any(not url.startswith(base) for url in urls):
        raise ValueError('Sitemap URLs must belong to the configured site and key location')
    for offset in range(0, len(urls), 10000):
        batch = urls[offset:offset + 10000]
        response = requests.post('https://api.indexnow.org/indexnow', json={
            'host': urlparse(base).netloc,
            'key': api_key,
            'keyLocation': f'{base}{api_key}.txt',
            'urlList': batch,
        }, timeout=30)
        if response.status_code not in (200, 202):
            raise RuntimeError(f'IndexNow submission failed: HTTP {response.status_code}')
        suffix = ' (key validation pending)' if response.status_code == 202 else ''
        print(f'IndexNow received {len(batch)} URLs{suffix}; indexing is not guaranteed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sitemap', type=Path, default=Path('dist/site/sitemap.xml'))
    parser.add_argument('--indexnow-key', type=Path, required=True)
    parser.add_argument('--site-url', default='https://hku.jacobshing.com/')
    args = parser.parse_args()
    try:
        urls = get_urls_to_index(args.sitemap)
        if not urls:
            raise ValueError('No page URLs found in sitemap')
        submit_to_indexnow(urls, args.indexnow_key.read_text().strip(), args.site_url)
    except (OSError, ValueError, RuntimeError, ET.ParseError, requests.RequestException) as error:
        print(f'IndexNow error: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
