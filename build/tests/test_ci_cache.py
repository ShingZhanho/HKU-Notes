"""CI must skip compiler setup only after verifying source and artifact contents."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from hkbuild.document import build
from hkbuild.metadata import REPOSITORY

spec = importlib.util.spec_from_file_location('ci_cache', REPOSITORY / 'build/ci-cache.py')
ci_cache = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci_cache)


class CICacheTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.doc = self.root / 'DOC'
        self.doc.mkdir()
        self.artifacts = self.root / 'artifacts'
        self.metadata = {'$schema': '../../site/docs/statics/schemas/v3.json', 'build': {
            'type': 'custom', 'output_file': 'result.txt', 'steps': [{'type': 'command', 'argv': [
                '{python}', '-c', "from pathlib import Path; Path('result.txt').write_text(Path('input.txt').read_text())"]}]}}
        self.write_metadata()
        (self.doc / 'input.txt').write_text('source')

    def write_metadata(self):
        (self.doc / 'metadata.json').write_text(json.dumps(self.metadata))

    def required(self, force=False):
        return ci_cache.needs_compilation(self.doc, self.artifacts, force)[0]

    def test_warm_cache_restores_without_any_compiler(self):
        self.assertTrue(self.required())
        build(self.doc, self.artifacts)
        (self.doc / 'result.txt').unlink()
        with patch('hkbuild.document.check_tools', side_effect=AssertionError('compiler check')), \
             patch('hkbuild.document.run', side_effect=AssertionError('compiler execution')):
            self.assertFalse(self.required())
            build(self.doc, self.artifacts)
        self.assertEqual((self.doc / 'result.txt').read_text(), 'source')

    def test_changed_source_corruption_and_force_require_compiler(self):
        build(self.doc, self.artifacts)
        self.assertTrue(self.required(force=True))
        (self.doc / 'input.txt').write_text('changed')
        self.assertTrue(self.required())
        (self.doc / 'input.txt').write_text('source')
        self.assertFalse(self.required())
        (self.artifacts / 'DOC/result.txt').write_text('corrupt')
        self.assertTrue(self.required())

    def test_cache_disabled_and_page_target(self):
        self.metadata['build']['cache'] = False
        self.write_metadata()
        build(self.doc, self.artifacts)
        self.assertTrue(self.required())
        self.metadata['build'] = {'type': 'page'}
        self.write_metadata()
        self.assertFalse(self.required(force=True))
