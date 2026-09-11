"""Repeatable static-site assembly with no deployment or remote artifact access."""
import json
from pathlib import Path
import shutil
import sys
from urllib.parse import urlparse

from .document import digest, inside, run
from .metadata import load
from generate_nav import generate as generate_nav
from generate_sitemap import generate as generate_sitemap
from page_gen_tools import start
from page_gen_tools.pdf_preview import embed_previews
from page_gen_tools.paths import SitePaths


def assemble(repository, targets, artifacts, site_url):
    if urlparse(site_url).scheme not in ('http', 'https') or not urlparse(site_url).netloc:
        raise ValueError('--site-url must be an absolute http(s) URL')
    staging = repository / '.build/site'
    destination = repository / 'dist/site'
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    for name in ('docs', 'overrides'):
        source = repository / 'site' / name
        if source.exists():
            shutil.copytree(source, staging / name)
    paths = SitePaths(repository, staging / 'docs', artifacts)
    files = paths.docs / 'files'
    if files.exists():
        shutil.rmtree(files)
    files.mkdir()
    for target in targets:
        spec = load(paths.metadata(target))['build']
        if spec['type'] == 'alias':
            continue
        manifest_path = artifacts / target / 'manifest.json'
        manifest = json.loads(manifest_path.read_text())
        expected = {} if spec['type'] == 'page' else {'primary': spec['output_file'], **spec.get('outputs', {})}
        if manifest['target'] != target or {k: v['path'] for k, v in manifest['outputs'].items()} != expected:
            raise ValueError(f'Artifacts do not match current metadata for {target}; rebuild the target')
        for entry in manifest['outputs'].values():
            source = inside(artifacts / target, entry['path'])
            if digest(source) != entry['sha256']:
                raise ValueError(f'Artifact checksum mismatch: {source}')
            output = inside(files / target, entry['path'])
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, output)
    start(targets, paths)
    generate_nav(targets, repository, repository / 'site/mkdocs.yml', staging / 'mkdocs.yml', site_url)
    run([sys.executable, '-m', 'zensical', 'build'], staging)
    output = staging / 'output'
    if not (output / 'index.html').is_file():
        raise ValueError('Zensical did not produce output/index.html')
    embed_previews(output)
    generate_sitemap(targets, paths, output, site_url)
    for file in (repository / 'build/seo').iterdir():
        if file.is_file():
            shutil.copy2(file, output / file.name)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(output, destination)
    print(f'Website built at {destination}')
