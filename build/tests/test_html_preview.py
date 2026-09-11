import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from hkbuild.document import digest
from hkbuild.html_preview import preview
from page_gen_tools.pdf_preview import render_preview, embed_previews

FIXTURE = '''<!doctype html><html><head><link rel="stylesheet" href="document.css"></head><body>
<script>fetch('remote-service')</script><div id="page-container"><div id="pf1" class="pf w0 h0"><div class="pc"><div class="t ff1">Complete searchable sentence.</div><img src="bg1.png"></div></div><div id="pf2" class="pf w0 h0"><div class="pc">Last page text.</div></div></div></body></html>'''
CSS = '@font-face{font-family:ff1;src:url(f1.woff)}.ff1{font-family:ff1}.w0{width:600px}.h0{height:800px}.pc{display:none}'


def fixture(destination):
    (destination / 'document.html').write_text(FIXTURE)
    (destination / 'document.css').write_text(CSS)
    (destination / 'bg1.png').write_bytes(b'image')
    (destination / 'f1.woff').write_bytes(b'font')


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'doc.pdf').write_bytes(b'pdf')
        (self.root / 'manifest.json').write_text(json.dumps({'target': 'DOC', 'outputs': {'primary': {'path': 'doc.pdf', 'sha256': digest(self.root / 'doc.pdf')}}}))

    def convert(self, pdf, destination, native):
        fixture(destination)

    def test_cache_invalidates_changed_asset_and_converter_but_not_unchanged_pdf(self):
        with patch('hkbuild.html_preview.backend', return_value=(['converter'], 'v1')), patch('hkbuild.html_preview.convert', side_effect=self.convert) as convert:
            preview(self.root)
            preview(self.root)
            self.assertEqual(convert.call_count, 1)
            (self.root / '~preview/f1.woff').write_bytes(b'corrupted')
            preview(self.root)
            self.assertEqual(convert.call_count, 2)
        with patch('hkbuild.html_preview.backend', return_value=(['converter'], 'v2')), patch('hkbuild.html_preview.convert', side_effect=self.convert) as convert:
            preview(self.root)
            convert.assert_called_once()
        self.assertNotIn('<script', (self.root / '~preview/document.html').read_text())

    def test_failure_preserves_previous_preview(self):
        with patch('hkbuild.html_preview.backend', return_value=(['converter'], 'v1')), patch('hkbuild.html_preview.convert', side_effect=self.convert):
            preview(self.root)
        before = (self.root / '~preview/document.html').read_bytes()
        with patch('hkbuild.html_preview.backend', return_value=(['converter'], 'v2')), patch('hkbuild.html_preview.convert', side_effect=RuntimeError('failed')):
            with self.assertRaises(RuntimeError): preview(self.root)
        self.assertEqual(before, (self.root / '~preview/document.html').read_bytes())

    def test_shadow_markup_contains_every_page_and_isolates_fonts(self):
        fixture(self.root)
        result = render_preview('DOC', self.root)
        self.assertIn('shadowrootmode="open"', result)
        self.assertIn('Complete searchable sentence.', result)
        self.assertIn('Last page text.', result)
        self.assertIn('DOC~preview/bg1.png', result)
        self.assertIn('url("DOC~preview/f1.woff")', result)
        self.assertNotIn('<script', result)
        self.assertNotIn('<iframe', result)
        self.assertNotIn('font-family:ff1', result)
        self.assertNotIn('@font-face', result.split('<template')[1])

    def test_embedding_removes_duplicate_preview_html(self):
        details = self.root / 'downloads/details'
        directory = details / 'DOC~preview'
        directory.mkdir(parents=True)
        fixture(directory)
        page = details / 'DOC.html'
        page.write_text('<main><div data-html-preview="DOC"></div></main>')
        embed_previews(self.root)
        self.assertIn('Last page text.', page.read_text())
        self.assertFalse((directory / 'document.html').exists())
        self.assertTrue((directory / 'f1.woff').exists())
