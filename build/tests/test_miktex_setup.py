"""Exercise setup failure handling without changing the host MiKTeX installation."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from hkbuild.metadata import REPOSITORY

# Shell functions take precedence over PATH, including the user's real ~/bin.
HARNESS = r'''
miktexsetup() { echo "setup $*" >> "$TEST_LOG"; }
initexmf() {
    echo "initexmf $*" >> "$TEST_LOG"
    if [ "$1" = --mkmaps ] && [ "$TEST_MISSING_PACKAGE" != fontmap ]; then
        echo 'SimpleIcons--simpleiconstwo SimpleIcons <SimpleIcons.pfb' > "$TEST_FILES/pdftex.map"
    fi
}
miktex() {
    echo "miktex $*" >> "$TEST_LOG"
    if [ "$1" = packages ] && [ "$2" = install ]; then
        [ "$#" -eq 3 ] || return 88
        case "$3" in *,*) return 89 ;; esac
        if [ "$3" = "$TEST_FAIL_PACKAGE" ]; then return 7; fi
        if [ "$3" != "$TEST_MISSING_PACKAGE" ]; then
            : > "$TEST_FILES/$3.sty"
            if [ "$3" = simpleicons ]; then
                : > "$TEST_FILES/simpleicons.map"
                : > "$TEST_FILES/SimpleIcons.pfb"
            fi
        fi
    fi
}
kpsewhich() {
    if [ "$TEST_LOOKUP_MODE" = empty ]; then return 0; fi
    if [ "$TEST_LOOKUP_MODE" = error ]; then return 1; fi
    # Deliberately report even nonexistent paths to test the file-existence guard.
    echo "$TEST_FILES/$1"
}
. "$TEST_SETUP"
'''


class MiktexSetupTests(unittest.TestCase):
    def invoke(self, missing='', fail='', lookup='normal'):
        with tempfile.TemporaryDirectory(prefix='miktex setup ') as temporary:
            root = Path(temporary)
            env = {**os.environ, 'TEST_LOG': str(root / 'calls'), 'TEST_FILES': str(root),
                   'TEST_SETUP': str(REPOSITORY / 'build/setup-miktex.sh'),
                   'TEST_MISSING_PACKAGE': missing, 'TEST_FAIL_PACKAGE': fail,
                   'TEST_LOOKUP_MODE': lookup}
            result = subprocess.run(['sh', '-c', HARNESS], env=env, text=True, capture_output=True)
            return result, (root / 'calls').read_text().splitlines()

    def test_individual_installs_and_verified_styles(self):
        result, calls = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        for package in ['latexmk', 'texcount', 'xkeyval', 'kvsetkeys', 'iftex', 'kvoptions', 'simpleicons']:
            self.assertIn(f'miktex packages install {package}', calls)
        for package in ['xkeyval', 'kvsetkeys', 'iftex', 'kvoptions']:
            self.assertIn(f'Verified {package}.sty:', result.stdout)
        self.assertLess(calls.index('miktex packages update'), calls.index('miktex packages install xkeyval'))
        self.assertLess(calls.index('miktex packages install kvoptions'), calls.index('initexmf --update-fndb'))

    def test_zero_exit_install_that_did_not_install_is_rejected(self):
        result, _ = self.invoke(missing='xkeyval')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('xkeyval.sty is still missing', result.stderr)

    def test_installer_failure_stops_setup(self):
        result, calls = self.invoke(fail='xkeyval')
        self.assertEqual(result.returncode, 7)
        self.assertNotIn('initexmf --mkmaps', calls)

    def test_empty_and_failed_lookup_are_rejected(self):
        for mode in ['empty', 'error']:
            with self.subTest(mode=mode):
                result, _ = self.invoke(lookup=mode)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('xkeyval.sty is still missing', result.stderr)

    def test_font_install_precedes_map_generation(self):
        result, calls = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLess(calls.index('miktex packages install simpleicons'), calls.index('initexmf --mkmaps'))
        self.assertIn('Verified SimpleIcons', result.stdout)

    def test_missing_font_files_or_active_mapping_are_rejected(self):
        for missing in ['simpleicons', 'fontmap']:
            with self.subTest(missing=missing):
                result, _ = self.invoke(missing=missing)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('MiKTeX setup failed:', result.stderr)
