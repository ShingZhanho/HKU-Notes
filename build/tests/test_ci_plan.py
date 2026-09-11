"""Keep branch selection and alias handling consistent across matrix and site jobs."""
import importlib.util
import unittest

from hkbuild.metadata import REPOSITORY, resolve_alias
from hkbuild.targets import select

spec = importlib.util.spec_from_file_location('ci_plan', REPOSITORY / 'build/ci-plan.py')
ci_plan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci_plan)


class CIPlanTests(unittest.TestCase):
    def test_full_site_has_one_job_per_canonical_target(self):
        result = ci_plan.plan('master')
        self.assertEqual(result['targets'], select(REPOSITORY))
        jobs = result['matrix']['target']
        self.assertEqual(len(jobs), len(set(jobs)))
        self.assertEqual(set(jobs), {resolve_alias(REPOSITORY / 'src' / name).name for name in result['targets']})
        self.assertIn('ENGG1340-Cheatsheet', result['targets'])
        self.assertNotIn('ENGG1340-Cheatsheet', jobs)

    def test_target_branch_preserves_alias_for_site(self):
        result = ci_plan.plan('targets/ENGG1340-Cheatsheet/fix')
        self.assertEqual(result['targets'], ['COMP2113-Cheatsheet', 'ENGG1340-Cheatsheet'])
        self.assertEqual(result['matrix'], {'target': ['COMP2113-Cheatsheet']})

    def test_invalid_branch_target_fails_before_matrix(self):
        with self.assertRaises(ValueError):
            ci_plan.plan('targets/../fix')

    def test_ordinary_branch_selects_full_site(self):
        self.assertEqual(ci_plan.plan('feature/build'), ci_plan.plan('master'))
