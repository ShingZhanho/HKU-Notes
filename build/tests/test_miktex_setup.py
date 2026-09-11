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
initexmf() { echo "initexmf $*" >> "$TEST_LOG"; }
sleep() { echo "sleep $*" >> "$TEST_LOG"; }
miktex() {
    echo "miktex $*" >> "$TEST_LOG"
    if [ "$1" = packages ] && [ "$2" = info ]; then
        if [ -f "$TEST_FILES/$4.sty" ]; then echo true; else echo false; fi
    fi
    if [ "$1" = packages ] && [ "$2" = install ]; then
        if [ -f "$TEST_FILES/$3.sty" ]; then return 1; fi
        [ "$#" -eq 3 ] || return 88
        case "$3" in *,*) return 89 ;; esac
        if [ "$3" = "$TEST_FAIL_PACKAGE" ]; then return 7; fi
        if [ "$3" != "$TEST_MISSING_PACKAGE" ]; then
            : > "$TEST_FILES/$3.sty"
            if [ "$3" = "$TEST_PARTIAL_PACKAGE" ]; then return 7; fi
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
    def invoke(self, missing='', fail='', lookup='normal', warm=(), twice=False, partial=''):
        with tempfile.TemporaryDirectory(prefix='miktex setup ') as temporary:
            root = Path(temporary)
            for package in warm:
                (root / (package + '.sty')).touch()
            env = {**os.environ, 'TEST_LOG': str(root / 'calls'), 'TEST_FILES': str(root),
                   'TEST_SETUP': str(REPOSITORY / 'build/setup-miktex.sh'),
                   'TEST_MISSING_PACKAGE': missing, 'TEST_FAIL_PACKAGE': fail,
                   'TEST_LOOKUP_MODE': lookup, 'TEST_PARTIAL_PACKAGE': partial}
            harness = HARNESS + ('\n. \"$TEST_SETUP\"\n' if twice else '')
            result = subprocess.run(['sh', '-c', harness], env=env, text=True, capture_output=True)
            return result, (root / 'calls').read_text().splitlines()

    def test_individual_installs_and_verified_styles(self):
        result, calls = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        for package in ['latexmk', 'texcount', 'xkeyval', 'kvsetkeys', 'iftex', 'kvoptions']:
            self.assertIn(f'miktex packages install {package}', calls)
        for package in ['xkeyval', 'kvsetkeys', 'iftex', 'kvoptions']:
            self.assertIn(f'Verified {package}.sty:', result.stdout)
        self.assertLess(calls.index('miktex packages update'), calls.index('miktex packages install xkeyval'))
        self.assertLess(calls.index('miktex packages install kvoptions'), calls.index('initexmf --enable-installer --update-fndb'))

    def test_zero_exit_install_that_did_not_install_is_rejected(self):
        result, _ = self.invoke(missing='xkeyval')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('xkeyval.sty is still missing', result.stderr)

    def test_installer_failure_stops_setup(self):
        result, calls = self.invoke(fail='xkeyval')
        self.assertEqual(result.returncode, 7)
        self.assertNotIn('initexmf --enable-installer --mkmaps', calls)

    def test_empty_and_failed_lookup_are_rejected(self):
        for mode in ['empty', 'error']:
            with self.subTest(mode=mode):
                result, _ = self.invoke(lookup=mode)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('xkeyval.sty is still missing', result.stderr)

    def test_no_font_specific_preinstallation(self):
        result, calls = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        installs = [line.split()[-1] for line in calls if line.startswith('miktex packages install ')]
        self.assertEqual(installs, ['latexmk', 'texcount', 'xkeyval', 'kvsetkeys', 'iftex', 'kvoptions'])
        self.assertIn('initexmf --enable-installer --mkmaps', calls)

    def test_retry_budget_is_bounded(self):
        result, calls = self.invoke(fail='texcount')
        self.assertEqual(result.returncode, 7)
        self.assertEqual(calls.count('miktex packages install texcount'), 3)
        self.assertEqual([line for line in calls if line.startswith('sleep')], ['sleep 5', 'sleep 10'])

    def test_warm_cache_skips_already_installed_packages(self):
        packages = ['latexmk', 'texcount', 'xkeyval', 'kvsetkeys', 'iftex', 'kvoptions']
        result, calls = self.invoke(warm=packages)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(any(line.startswith('miktex packages install') for line in calls))
        self.assertIn('Verified xkeyval.sty:', result.stdout)

    def test_partial_cache_installs_only_missing_packages(self):
        result, calls = self.invoke(warm=['latexmk', 'xkeyval'])
        self.assertEqual(result.returncode, 0, result.stderr)
        installs = [line.split()[-1] for line in calls if line.startswith('miktex packages install')]
        self.assertEqual(installs, ['texcount', 'kvsetkeys', 'iftex', 'kvoptions'])

    def test_setup_can_run_twice(self):
        result, calls = self.invoke(twice=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls.count('miktex packages install latexmk'), 1)
        self.assertEqual(calls.count('initexmf --enable-installer --mkmaps'), 2)

    def test_retry_rechecks_state_after_partial_success(self):
        result, calls = self.invoke(partial='latexmk')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls.count('miktex packages install latexmk'), 1)
        self.assertIn('Already installed: latexmk', result.stdout)
