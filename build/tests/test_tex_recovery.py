import subprocess
import sys
import io
from contextlib import redirect_stdout
import unittest
from unittest.mock import patch

from hkbuild import document


class TexRecoveryTests(unittest.TestCase):
    def exercise(self, diagnostics, version='MiKTeX 26.5', maintenance_failures=0):
        calls = []
        remaining = iter(diagnostics)
        def run(argv, cwd=None, capture=False):
            nonlocal maintenance_failures
            calls.append(list(argv))
            if argv[0] == 'latexmk':
                message = next(remaining, None)
                if message:
                    raise subprocess.CalledProcessError(12, argv, output=message)
            elif '--version' in argv:
                return subprocess.CompletedProcess(argv, 0, stdout=version)
            elif argv[0] == 'initexmf' and maintenance_failures:
                maintenance_failures -= 1
                raise subprocess.CalledProcessError(1, argv)
            return subprocess.CompletedProcess(argv, 0)
        error = None
        with patch.object(document, 'run', run), patch.object(document.time, 'sleep'):
            try:
                document.compile_latex(['latexmk', '-pdf', '-halt-on-error', '-cd', 'main.tex'], '.', 'pdflatex')
            except subprocess.CalledProcessError as failure:
                error = failure
        return calls, error

    def test_any_font_recovers_after_map_refresh(self):
        for font in ['fa5brands0', 'SimpleIcons--simpleiconstwo', 'arbitrary-new-font']:
            with self.subTest(font=font):
                calls, error = self.exercise([f'Font {font} at 600 not found'])
                self.assertIsNone(error)
                self.assertEqual(calls[2:4], [['initexmf', '--enable-installer', '--update-fndb'], ['initexmf', '--enable-installer', '--mkmaps']])
                self.assertIn('-g', calls[-1])
                self.assertIn('-halt-on-error', calls[-1])
                self.assertNotIn('-f', calls[-1])

    def test_network_failure_recovers(self):
        calls, error = self.exercise(['Sorry, but pdflatex did not succeed.'])
        self.assertIsNone(error)
        self.assertEqual(sum(c[0] == 'latexmk' for c in calls), 2)

    def test_persistent_failure_remains_failure(self):
        calls, error = self.exercise(['Timeout was reached'] * 3)
        self.assertIsNotNone(error)
        self.assertEqual(sum(c[0] == 'latexmk' for c in calls), 3)

    def test_source_errors_do_not_retry(self):
        calls, error = self.exercise(['Undefined control sequence.'])
        self.assertIsNotNone(error)
        self.assertEqual(len(calls), 1)

    def test_texlive_does_not_run_miktex_maintenance(self):
        calls, error = self.exercise(['Font example not found'], version='TeX Live 2026')
        self.assertIsNotNone(error)
        self.assertFalse(any(c[0] == 'initexmf' for c in calls))

    def test_maintenance_network_failure_retries(self):
        calls, error = self.exercise(['Font example not found'], maintenance_failures=1)
        self.assertIsNone(error)
        self.assertEqual(sum('--update-fndb' in c for c in calls), 2)

    def test_failed_maintenance_is_not_ignored(self):
        calls, error = self.exercise(['Font example not found'], maintenance_failures=3)
        self.assertIsNotNone(error)
        self.assertEqual(sum(c[0] == 'latexmk' for c in calls), 1)

    def test_live_runner_preserves_both_output_streams_on_failure(self):
        with redirect_stdout(io.StringIO()) as output:
            with self.assertRaises(subprocess.CalledProcessError) as caught:
                document.run([sys.executable, '-c', "import sys; print('font failure'); print('detail', file=sys.stderr); sys.exit(7)"], capture='tee')
        self.assertEqual(caught.exception.returncode, 7)
        for text in ['font failure', 'detail']:
            self.assertIn(text, caught.exception.output)
            self.assertIn(text, output.getvalue())

    def test_live_runner_tolerates_mixed_encodings_and_preserves_exit_status(self):
        for status in [0, 12]:
            with self.subTest(status=status), redirect_stdout(io.StringIO()) as output:
                mixed = b'French: ' + bytes([233]) + '; UTF-8: é'.encode('utf-8') + bytes([10])
                command = [sys.executable, '-c',
                           f"import os, sys; os.write(1, {mixed!r}); "
                           f"print('Font example not found', file=sys.stderr); sys.exit({status})"]
                if status:
                    with self.assertRaises(subprocess.CalledProcessError) as caught:
                        document.run(command, capture='tee')
                    self.assertEqual(caught.exception.returncode, status)
                    diagnostic = caught.exception.output
                else:
                    result = document.run(command, capture='tee')
                    self.assertEqual(result.returncode, 0)
                    diagnostic = result.stdout
                self.assertIn('French: \ufffd; UTF-8: é', diagnostic)
                self.assertIn('Font example not found', diagnostic)
                self.assertIn(diagnostic, output.getvalue())
