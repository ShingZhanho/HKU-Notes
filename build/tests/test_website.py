import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from hkbuild.document import build, digest
from hkbuild.metadata import REPOSITORY
from hkbuild.website import assemble
from test_html_preview import fixture


class WebsiteTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='hku site ')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(REPOSITORY / 'site', self.root / 'site', ignore=shutil.ignore_patterns('output', '.cache'))
        (self.root / 'build/seo').mkdir(parents=True)
        shutil.copy2(REPOSITORY / 'build/course-codes.sqlite', self.root / 'build/course-codes.sqlite')
        for name, spec in [('DOC', {'type': 'custom', 'output_file': 'report.pdf', 'steps': []}), ('PAGE', {'type': 'page'}), ('ALIAS', {'type': 'alias', 'target': 'DOC'}), ('ALIAS2', {'type': 'alias', 'target': 'ALIAS'})]:
            directory = self.root / 'src' / name
            directory.mkdir(parents=True)
            (directory / 'metadata.json').write_text(json.dumps({'$schema': '../../site/docs/statics/schemas/v3.json', 'build': spec, 'static_site': {'description': 'Description: with punctuation'}}))
        (self.root / 'src/DOC/report.pdf').write_bytes(b'PDF fixture')
        self.artifacts = self.root / 'artifacts'
        for name in ['DOC', 'PAGE']:
            build(self.root / 'src' / name, self.artifacts)
        (self.artifacts / 'DOC/~preview').mkdir()
        fixture(self.artifacts / 'DOC/~preview')

    def fake_zensical(self, argv, cwd):
        self.assertEqual(argv[1:], ['-m', 'zensical', 'build'])
        shutil.copytree(cwd / 'docs', cwd / 'output')
        (cwd / 'output/index.html').write_text('<html><link rel="canonical" href="https://example.org/notes/index.html">home</html>')
        for name in ['DOC', 'PAGE']:
            (cwd / f'output/downloads/details/{name}.html').write_text('<div data-html-preview="DOC"></div>' if name == 'DOC' else 'page')

    def test_repeatable_and_does_not_modify_inputs(self):
        originals = {p: digest(p) for root in [self.root / 'site', self.artifacts] for p in root.rglob('*') if p.is_file()}
        def snapshot():
            return {str(p.relative_to(self.root / '.build/site/docs')): digest(p) for p in (self.root / '.build/site/docs').rglob('*') if p.is_file()}
        with patch('hkbuild.website.run', self.fake_zensical):
            assemble(self.root, ['DOC', 'PAGE', 'ALIAS', 'ALIAS2'], self.artifacts, 'https://example.org/notes/')
            first = snapshot()
            assemble(self.root, ['DOC', 'PAGE', 'ALIAS', 'ALIAS2'], self.artifacts, 'https://example.org/notes/')
            self.assertEqual(first, snapshot())
        self.assertEqual(originals, {p: digest(p) for p in originals})
        self.assertEqual((self.root / 'dist/site/files/DOC/report.pdf').read_bytes(), b'PDF fixture')
        sitemap = ET.parse(self.root / 'dist/site/sitemap.xml')
        urls = [item.text for item in sitemap.findall('.//{*}loc')]
        self.assertNotIn('https://example.org/notes/files/DOC/report.pdf', urls)
        self.assertIn('https://example.org/notes/index.html', urls)
        self.assertNotIn('https://example.org/notes/files/PAGE/NON_FILE_TARGET', urls)
        navigation = (self.root / '.build/site/mkdocs.yml').read_text()
        self.assertIn('"ALIAS2": downloads/details/DOC.md', navigation)
        self.assertIn('../../files/DOC/report.pdf', (self.root / '.build/site/docs/downloads/details/DOC.md').read_text())

    def test_changed_artifact_rejected(self):
        (self.artifacts / 'DOC/report.pdf').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            assemble(self.root, ['DOC'], self.artifacts, 'https://example.org/')

    def test_failed_site_build_preserves_previous_output(self):
        (self.root / 'dist/site').mkdir(parents=True)
        (self.root / 'dist/site/index.html').write_text('previous site')
        with patch('hkbuild.website.run', side_effect=ValueError('site failed')):
            with self.assertRaisesRegex(ValueError, 'site failed'):
                assemble(self.root, ['DOC'], self.artifacts, 'https://example.org/')
        self.assertEqual((self.root / 'dist/site/index.html').read_text(), 'previous site')
