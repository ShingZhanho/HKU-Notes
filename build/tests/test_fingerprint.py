import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from hkbuild.document import build
from hkbuild.fingerprint import fingerprint
from hkbuild.metadata import load

SCHEMA = '../../site/docs/statics/schemas/v3.json'


class FingerprintTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.doc = self.root / 'first/notes'
        self.doc.mkdir(parents=True)
        self.artifacts = self.root / 'artifacts'
        self.data = {'$schema': SCHEMA, 'build': {'type': 'custom', 'output_file': 'result.txt', 'steps': [
            {'type': 'command', 'argv': ['{python}', '-c', "from pathlib import Path; Path('result.txt').write_text(Path('input.txt').read_text()); p=Path('.build/count'); p.write_text(str(int(p.read_text())+1) if p.exists() else '1')"]}]}}
        self.write_metadata()
        (self.doc / 'input.txt').write_text('one')

    def write_metadata(self):
        (self.doc / 'metadata.json').write_text(json.dumps(self.data))

    def key(self, override=None):
        return fingerprint(self.doc, load(self.doc / 'metadata.json')['build'], source_override=override)

    def test_skip_unchanged_even_after_touch_and_restore_deleted_output(self):
        build(self.doc, self.artifacts)
        (self.doc / 'input.txt').touch()
        (self.doc / 'result.txt').unlink()
        with patch('hkbuild.document.run', side_effect=AssertionError('compiler must not run')):
            build(self.doc, self.artifacts)
        self.assertEqual((self.doc / 'result.txt').read_text(), 'one')
        self.assertEqual((self.doc / '.build/count').read_text(), '1')

    def test_reuse_across_checkout_paths(self):
        build(self.doc, self.artifacts)
        other = self.root / 'second/notes'
        other.mkdir(parents=True)
        for name in ('input.txt', 'metadata.json'):
            shutil.copy2(self.doc / name, other / name)
        with patch('hkbuild.document.run', side_effect=AssertionError('compiler must not run')):
            build(other, self.artifacts)
        self.assertEqual((other / 'result.txt').read_text(), 'one')

    def test_source_changes_additions_and_deletions_change_key(self):
        first = self.key()
        (self.doc / 'input.txt').write_text('two')
        second = self.key()
        self.assertNotEqual(first, second)
        (self.doc / 'new.txt').write_text('new')
        self.assertNotEqual(second, self.key())
        (self.doc / 'new.txt').unlink()
        self.assertEqual(second, self.key())
        (self.doc / 'input.txt').unlink()
        self.assertNotEqual(second, self.key())

    def test_ignore_patterns_negation_and_protected_metadata(self):
        self.data['build']['hash_ignore'] = ['scratch/**', '!scratch/required.txt', 'metadata.json']
        self.write_metadata()
        (self.doc / 'scratch').mkdir()
        (self.doc / 'scratch/required.txt').write_text('required')
        first = self.key()
        (self.doc / 'scratch/notes.txt').write_text('ignored')
        self.assertEqual(first, self.key())
        (self.doc / 'scratch/required.txt').write_text('changed')
        self.assertNotEqual(first, self.key())
        second = self.key()
        self.data['static_site'] = {'description': 'Metadata remains protected'}
        self.write_metadata()
        self.assertNotEqual(second, self.key())

    def test_ignored_edits_skip_execution_and_ignore_rule_edits_invalidate(self):
        self.data['build']['hash_ignore'] = ['scratch.txt']
        self.write_metadata()
        build(self.doc, self.artifacts)
        (self.doc / 'scratch.txt').write_text('ignored')
        build(self.doc, self.artifacts)
        self.assertEqual((self.doc / '.build/count').read_text(), '1')
        self.data['build']['hash_ignore'] = []
        self.write_metadata()
        build(self.doc, self.artifacts)
        self.assertEqual((self.doc / '.build/count').read_text(), '2')

    def test_input_pdf_is_hashed_but_generated_output_is_not(self):
        first = self.key()
        (self.doc / 'result.txt').write_text('generated')
        (self.doc / 'notes.aux').write_text('auxiliary')
        self.assertEqual(first, self.key())
        (self.doc / 'figure.pdf').write_bytes(b'input PDF')
        self.assertNotEqual(first, self.key())

    def test_corrupt_or_missing_artifact_rebuilds(self):
        build(self.doc, self.artifacts)
        output = self.artifacts / 'notes/result.txt'
        output.write_text('corrupt')
        build(self.doc, self.artifacts)
        self.assertEqual(output.read_text(), 'one')
        self.assertEqual((self.doc / '.build/count').read_text(), '2')
        output.unlink()
        build(self.doc, self.artifacts)
        self.assertEqual((self.doc / '.build/count').read_text(), '3')

    def test_force_and_cache_disabled(self):
        build(self.doc, self.artifacts)
        build(self.doc, self.artifacts, force=True)
        self.assertEqual((self.doc / '.build/count').read_text(), '2')
        self.data['build']['cache'] = False
        self.write_metadata()
        build(self.doc, self.artifacts)
        build(self.doc, self.artifacts)
        self.assertEqual((self.doc / '.build/count').read_text(), '4')

    def test_source_override_changes_are_hashed(self):
        override = self.root / 'override'
        override.mkdir()
        (override / 'input.tex').write_text('one')
        first = self.key(override)
        (override / 'input.tex').write_text('two')
        self.assertNotEqual(first, self.key(override))

    def test_failed_forced_build_removes_old_manifest(self):
        build(self.doc, self.artifacts)
        with patch('hkbuild.document.run', side_effect=ValueError('failure')):
            with self.assertRaisesRegex(ValueError, 'failure'):
                build(self.doc, self.artifacts, force=True)
        self.assertFalse((self.artifacts / 'notes/manifest.json').exists())

    def test_supplied_artifact_does_not_acquire_source_provenance(self):
        supplied = self.root / 'supplied/notes'
        supplied.mkdir(parents=True)
        (supplied / 'result.txt').write_text('unrelated')
        build(self.doc, self.artifacts, artifact_input=supplied.parent)
        manifest = json.loads((self.artifacts / 'notes/manifest.json').read_text())
        self.assertIsNone(manifest['source_fingerprint'])
        build(self.doc, self.artifacts)
        self.assertEqual((self.doc / 'result.txt').read_text(), 'one')
