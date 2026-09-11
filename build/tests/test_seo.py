from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import xml.etree.ElementTree as ET

from generate_sitemap import generate
from request_indexing import get_urls_to_index, submit_to_indexnow


class SEOTests(unittest.TestCase):
    def test_sitemap_uses_only_local_canonical_indexable_pages(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pages = {
                'index.html': '<link rel="canonical" href="https://example.org/notes/">',
                'doc.html': '<link rel="canonical" href="https://example.org/notes/doc.html">',
                'duplicate.html': '<link rel="canonical" href="https://example.org/notes/doc.html">',
                'external.html': '<link rel="canonical" href="https://other.org/external.html">',
                '404.html': '<link rel="canonical" href="https://example.org/notes/404.html">',
                'private.html': '<link rel="canonical" href="https://example.org/notes/private.html"><meta name="robots" content="follow, noindex">',
                'verification.html': 'google-site-verification: verification.html',
                'converter.html': '<html>raw converter output</html>',
            }
            for name, html in pages.items():
                (root / name).write_text(html)
            (root / 'sitemap.xml.gz').write_bytes(b'stale')
            generate([], None, root, 'https://example.org/notes/')
            self.assertEqual(get_urls_to_index(root / 'sitemap.xml'),
                             ['https://example.org/notes/', 'https://example.org/notes/doc.html'])
            self.assertFalse((root / 'sitemap.xml.gz').exists())
            self.assertIn('Sitemap: https://example.org/notes/sitemap.xml', (root / 'robots.txt').read_text())

    @patch('request_indexing.requests.post')
    def test_indexnow_failure_is_not_reported_as_success(self, post):
        post.return_value = Mock(status_code=429)
        with self.assertRaisesRegex(RuntimeError, '429'):
            submit_to_indexnow(['https://example.org/doc.html'], 'abcdefgh', 'https://example.org/')

    @patch('request_indexing.requests.post')
    def test_indexnow_rejects_urls_outside_key_scope(self, post):
        for url in ['https://other.org/doc.html', 'https://example.org/other/doc.html']:
            with self.assertRaises(ValueError):
                submit_to_indexnow([url], 'abcdefgh', 'https://example.org/notes/')
        post.assert_not_called()

    @patch('request_indexing.requests.post')
    def test_indexnow_batches_and_accepts_pending_key_validation(self, post):
        post.return_value = Mock(status_code=202)
        urls = [f'https://example.org/{n}.html' for n in range(10001)]
        submit_to_indexnow(urls, 'abcdefgh', 'https://example.org/')
        self.assertEqual([len(c.kwargs['json']['urlList']) for c in post.call_args_list], [10000, 1])
