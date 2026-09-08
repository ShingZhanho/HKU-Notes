import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from hkbuild import document
from hkbuild.configure import main as configure

SCHEMA = '../../site/docs/statics/schemas/v3.json'


class DocumentTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='hku build $ space ')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.doc = self.root / 'notes'
        self.doc.mkdir()
        self.artifacts = self.root / 'artifacts'

    def metadata(self, spec):
        (self.doc / 'metadata.json').write_text(json.dumps({'$schema': SCHEMA, 'build': spec}))

    def command(self, code, **kwargs):
        return {'type': 'command', 'argv': ['{python}', '-c', code], **kwargs}

    def test_configure_make_repeat_and_dependency_change(self):
        (self.doc / 'input.txt').write_text('one')
        step = self.command("from pathlib import Path; p=Path('runs'); p.write_text(p.read_text()+'x' if p.exists() else 'x'); Path('result.txt').write_text(Path('input.txt').read_text())", inputs=['input.txt'], outputs=['result.txt'])
        self.metadata({'type': 'custom', 'output_file': 'result.txt', 'steps': [step]})
        with contextlib.chdir(self.doc), contextlib.redirect_stdout(io.StringIO()):
            configure([])
        for expected in ['one', 'one', 'two']:
            (self.doc / 'input.txt').write_text(expected)
            subprocess.run(['make'], cwd=self.doc, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual((self.doc / 'result.txt').read_text(), expected)
        self.assertEqual((self.doc / 'runs').read_text(), 'xx')
        subprocess.run(['make', 'distclean'], cwd=self.doc, check=True, stdout=subprocess.PIPE)
        self.assertFalse((self.doc / 'Makefile').exists())
        self.assertFalse((self.doc / 'result.txt').exists())
        self.assertTrue((self.doc / 'input.txt').exists())

    def test_failure_does_not_publish_stale_output(self):
        (self.doc / 'result.txt').write_text('old')
        self.metadata({'type': 'custom', 'output_file': 'result.txt', 'steps': [self.command('raise SystemExit(7)')]})
        with self.assertRaises(subprocess.CalledProcessError):
            document.build(self.doc, self.artifacts)
        self.assertFalse((self.artifacts / 'notes/manifest.json').exists())

    def test_missing_output_fails(self):
        self.metadata({'type': 'custom', 'output_file': 'missing.txt', 'steps': [self.command('pass')]})
        with self.assertRaisesRegex(ValueError, 'expected output is missing'):
            document.build(self.doc, self.artifacts)

    def test_alias_and_supplied_foreign_artifact(self):
        self.metadata({'type': 'alias', 'target': 'binary'})
        other = self.root / 'binary'
        other.mkdir()
        (other / 'metadata.json').write_text(json.dumps({'$schema': SCHEMA, 'build': {'type': 'custom', 'output_file': 'binary.zip', 'environment': {'os': 'windows'}, 'steps': []}}))
        inputs = self.root / 'supplied/binary'
        inputs.mkdir(parents=True)
        (inputs / 'binary.zip').write_bytes(b'artifact')
        document.build(self.doc, self.artifacts, artifact_input=inputs.parent)
        self.assertEqual((self.artifacts / 'binary/binary.zip').read_bytes(), b'artifact')

    def test_latex_rename_and_order(self):
        self.metadata({'type': 'latex', 'root_file': 'main.tex', 'output_file': 'renamed.pdf', 'prepare': [self.command("from pathlib import Path; Path('ready').touch()")], 'finish': [self.command("from pathlib import Path; assert Path('renamed.pdf').read_bytes() == b'%PDF-test'")]})
        (self.doc / 'main.tex').write_text('test')
        actual_run = document.run
        calls = []
        def fake_run(argv, cwd=None, capture=False):
            if argv[0] == 'latexmk':
                self.assertTrue((self.doc / 'ready').exists())
                calls.append(argv)
                (self.doc / 'main.pdf').write_bytes(b'%PDF-test')
            else:
                return actual_run(argv, cwd, capture)
        with patch.object(document, 'run', fake_run), patch.object(document, 'check_tools'):
            document.build(self.doc, self.artifacts)
        self.assertNotIn('-f', calls[0])
        self.assertIn('-halt-on-error', calls[0])
        self.assertEqual((self.artifacts / 'notes/renamed.pdf').read_bytes(), b'%PDF-test')

    def test_retries_tex_after_failure_without_ignoring_errors(self):
        self.metadata({'type': 'latex', 'root_file': 'main.tex'})
        (self.doc / 'main.tex').write_text('fixture')
        calls = []
        def compiler(argv, cwd=None, capture=False):
            calls.append(argv)
            if len(calls) == 1:
                raise subprocess.CalledProcessError(12, argv)
            (self.doc / 'main.pdf').write_bytes(b'%PDF-repaired')
        with patch.object(document, 'run', compiler), patch.object(document, 'check_tools'):
            with self.assertRaises(subprocess.CalledProcessError):
                document.build(self.doc, self.artifacts)
            document.build(self.doc, self.artifacts)
        self.assertNotIn('-g', calls[0])
        self.assertIn('-g', calls[1])
        self.assertNotIn('-f', calls[1])

    def test_checkout_is_pinned_and_reused_offline(self):
        upstream = self.root / 'upstream'
        upstream.mkdir()
        (upstream / 'file.txt').write_text('pinned')
        for args in [['git', 'init'], ['git', 'add', '.'], ['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.com', 'commit', '-m', 'fixture']]:
            subprocess.run(args, cwd=upstream, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=upstream, text=True).strip()
        spec = {'source': {'type': 'git', 'url': str(upstream), 'revision': revision}}
        source = document.source_root(self.doc, spec)
        upstream.rename(self.root / 'unavailable')
        self.assertEqual(document.source_root(self.doc, spec), source)
        self.assertEqual((source / 'file.txt').read_text(), 'pinned')

    def test_refuse_handwritten_makefile(self):
        self.metadata({'type': 'page'})
        (self.doc / 'Makefile').write_text('hand written')
        with contextlib.chdir(self.doc), self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            configure([])
        self.assertEqual((self.doc / 'Makefile').read_text(), 'hand written')

    def test_path_escape_rejected(self):
        with self.assertRaises(ValueError):
            document.inside(self.doc, '../outside')

class EnvironmentAndArtifactTests(unittest.TestCase):
    def test_incompatible_environment_is_rejected(self):
        with patch('platform.system', return_value='Darwin'), patch('platform.machine', return_value='arm64'):
            with self.assertRaisesRegex(ValueError, 'Required build environment'):
                document.check_environment({'environment': {'os': 'linux', 'architecture': 'x86_64', 'distribution': 'ubuntu', 'version': '24.04'}})

    def test_project_archive_contains_binary_and_resources(self):
        from hkbuild.metadata import REPOSITORY
        import zipfile
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            doc = root / 'document'
            source = root / 'source'
            doc.mkdir()
            (source / 'build/res').mkdir(parents=True)
            (source / 'build/shoot').write_bytes(b'fixture binary')
            (source / 'build/res/data.txt').write_text('fixture resource')
            script = doc / 'package.py'
            script.write_text((REPOSITORY / 'src/COMP2113-Project/package.py').read_text())
            subprocess.run([sys.executable, str(script)], cwd=source, check=True)
            with zipfile.ZipFile(doc / 'shoot-v1.0.0-ubuntu_24.04-x86_64.zip') as archive:
                self.assertEqual(set(archive.namelist()), {'shoot', 'res/data.txt'})
                self.assertEqual(archive.read('shoot'), b'fixture binary')


if __name__ == '__main__':
    unittest.main()
