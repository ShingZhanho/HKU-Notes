"""Execute provisioning with fake system commands; never modify host APT files."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from hkbuild.metadata import REPOSITORY

HARNESS = r'''
apt_get() {
    echo "$*" >> "$TEST_CALLS"
    if [ -f "$MIKTEX_APT_SOURCES" ]; then
        source=$(cat "$MIKTEX_APT_SOURCES")
        echo "$source" >> "$TEST_CALLS"
        case "$source" in
            *miktex.org*)
                case "$TEST_FAILURE" in
                    index|both) return 100 ;;
                    archive) case "$*" in *install*) return 100 ;; esac ;;
                esac ;;
            *mirrors.mit.edu*) [ "$TEST_FAILURE" != both ] || return 100 ;;
        esac
    fi
    return 0
}
alias apt-get=apt_get
curl() { return 0; }
gpg() { return 0; }
. "$TEST_SCRIPT"
'''


class UbuntuBootstrapTests(unittest.TestCase):
    def invoke(self, failure):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            env = {**os.environ, 'MIKTEX_APT_SOURCES': str(root / 'miktex.list'),
                   'TEST_CALLS': str(root / 'calls'), 'TEST_FAILURE': failure,
                   'TEST_SCRIPT': str(REPOSITORY / 'build/bootstrap-ubuntu.sh')}
            result = subprocess.run(['sh', '-c', HARNESS], env=env, capture_output=True, text=True)
            self.assertTrue((root / 'miktex.list').exists(), result.stderr)
            return result, (root / 'miktex.list').read_text(), (root / 'calls').read_text()

    def test_primary_success_does_not_use_fallback(self):
        result, source, calls = self.invoke('none')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('https://miktex.org/download/ubuntu', source)
        self.assertNotIn('mirrors.mit.edu', calls)

    def test_index_and_archive_failures_try_signed_fallback(self):
        for failure in ['index', 'archive']:
            with self.subTest(failure=failure):
                result, source, calls = self.invoke(failure)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('https://mirrors.mit.edu/CTAN/', source)
                self.assertIn('signed-by=/usr/share/keyrings/miktex.gpg', source)
                self.assertIn('APT::Update::Error-Mode=any', calls)

    def test_both_mirrors_failing_is_fatal(self):
        result, _, _ = self.invoke('both')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Unable to install MiKTeX', result.stderr)
