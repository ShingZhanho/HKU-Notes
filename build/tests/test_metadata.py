import json
from pathlib import Path
import tempfile
import unittest
from hkbuild.metadata import load, resolve_alias, REPOSITORY


class MetadataTests(unittest.TestCase):
    def test_all_repository_metadata(self):
        files = list((REPOSITORY / 'src').glob('*/metadata.json'))
        self.assertGreater(len(files), 30)
        for file in files:
            with self.subTest(file=file):
                load(file)
                resolve_alias(file.parent)

    def test_reject_legacy_and_unknown_fields(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'metadata.json'
            for data in ({'@metadata_file_version': '1'}, {'$schema': 'https://hku.jacobshing.com/statics/schemas/v2.json'},
                         {'$schema': '../../site/docs/statics/schemas/v3.json', 'build': {'type': 'latex', 'build_command': 'true'}}):
                path.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    load(path)

    def test_alias_cycle(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, target in [('a', 'b'), ('b', 'a')]:
                (root / name).mkdir()
                (root / name / 'metadata.json').write_text(json.dumps({'$schema': '../../site/docs/statics/schemas/v3.json', 'build': {'type': 'alias', 'target': target}}))
            with self.assertRaisesRegex(ValueError, 'Alias cycle'):
                resolve_alias(root / 'a')

    def test_profile_and_named_outputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'metadata.json'
            path.write_text(json.dumps({'$schema': '../../site/docs/statics/schemas/v3.json', 'build': {'type': 'latex'}, 'profiles': {'draft': {'output_file': 'draft.pdf', 'outputs': {'source': 'sources.zip'}}}}))
            self.assertEqual(load(path, 'draft')['build']['output_file'], 'draft.pdf')
            with self.assertRaisesRegex(ValueError, 'unknown profile'):
                load(path, 'missing')

    def test_reserved_or_duplicate_outputs_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'metadata.json'
            for outputs in ({'primary': 'other.pdf'}, {'other': 'main.pdf'}, {'other': 'metadata.json'}):
                path.write_text(json.dumps({'$schema': '../../site/docs/statics/schemas/v3.json', 'build': {'type': 'latex', 'output_file': 'main.pdf', 'outputs': outputs}}))
                with self.assertRaises(ValueError):
                    load(path)
