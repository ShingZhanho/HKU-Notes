"""Generate host-independent sitemaps, including downloadable artifacts."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
from urllib.parse import quote
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
    for file in output.rglob('*.html'):
        urls[str(file.relative_to(output))] = None
    images = {}
    for target in targets:
        metadata = load(paths.metadata(target))
        if metadata['build']['type'] == 'alias':
            continue
        lastmod = get_last_modified_datetime(target, paths.repository)
        urls[f'downloads/details/{target}.html'] = lastmod
        manifest = json.loads((paths.artifacts / target / 'manifest.json').read_text())
        for entry in manifest['outputs'].values():
            urls[f'files/{target}/{entry["path"]}'] = lastmod
        for file in (output / 'downloads/details' / f'{target}~preview').glob('*.png'):
            images[str(file.relative_to(output))] = lastmod
    urls['preview-images-sitemap.xml'] = None
    for filename, entries in [('sitemap.xml', urls), ('preview-images-sitemap.xml', images)]:
        tree = ET.Element(f'{{{NAMESPACE}}}urlset')
        for relative, modified in sorted(entries.items()):
            item = ET.SubElement(tree, f'{{{NAMESPACE}}}url')
            ET.SubElement(item, f'{{{NAMESPACE}}}loc').text = base + quote(relative, safe='/~')
            if modified:
                ET.SubElement(item, f'{{{NAMESPACE}}}lastmod').text = modified
        ET.ElementTree(tree).write(output / filename, encoding='utf-8', xml_declaration=True)
    (output / 'sitemap.xml.gz').unlink(missing_ok=True)
