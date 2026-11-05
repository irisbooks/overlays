"""Release continuity check regressions (no engine needed: iris is faked)."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('continuity', SCRIPTS / 'check-continuity.py')
CONTINUITY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTINUITY)

SUITE = '''cases:
  - name: carries the basis
    expect: {allocation_policy: "jp-example@2026.10.2#jp-example.shares"}
  - name: refuses another policy
    expect: {allocation_policy: "jp-example@2026.10.1#jp-example.shares"}
'''


def fake_iris(failing):
    """Pass every case except the named ones; record what the run saw."""
    seen = {}

    def run(candidate):
        results = []
        for suite in sorted((candidate / 'tests').glob('*.yaml')):
            seen[suite.name] = suite.read_text()
            for line in suite.read_text().splitlines():
                if line.strip().startswith('- name: '):
                    name = line.split('- name: ', 1)[1]
                    results.append({'suite': suite.name, 'name': name, 'passed': name not in failing,
                                    'failures': ['figures differ'] if name in failing else []})
        return results
    return run, seen


class Continuity(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.package = self.root / 'JP/jp-example'
        (self.package / 'tests').mkdir(parents=True)
        self.git('init', '-q')
        self.release('2026.10.2', SUITE)

    def git(self, *args):
        subprocess.run(['git', '-c', 'user.name=t', '-c', 'user.email=t@example.com', *args],
                       cwd=self.root, check=True, capture_output=True)

    def release(self, version, suite, tag=True):
        self.manifest(version)
        (self.package / 'tests/lifecycle.yaml').write_text(suite)
        self.git('add', '-A')
        self.git('commit', '-q', '-m', version, '--allow-empty')
        if tag:
            self.git('tag', '-a', f'jp-example@{version}', '-m', version)

    def manifest(self, version, extra=''):
        (self.package / 'overlay.yaml').write_text(f'id: jp-example\nversion: {version}\nrequires_bindings: 6\n{extra}')

    def check(self, failing=()):
        run, seen = fake_iris(set(failing))
        notes, errors = CONTINUITY.check(self.package, run=run, root=self.root)
        return notes, errors, seen

    def test_unreleased_or_unchanged_version_is_not_compared(self):
        notes, errors, seen = self.check()
        self.assertEqual(errors, [])
        self.assertIn('no new release', notes[0])
        self.assertEqual(seen, {})

    def test_new_release_runs_previous_suites_with_its_own_version(self):
        self.manifest('2026.11.1')
        (self.package / 'tests/lifecycle.yaml').write_text(SUITE.replace('2026.10.2#', '2026.11.1#'))
        notes, errors, seen = self.check()
        self.assertEqual(errors, [])
        previous = seen['previous-release.lifecycle.yaml']
        self.assertIn('jp-example@2026.11.1#jp-example.shares', previous)
        # Only the last release's own version is relabelled.
        self.assertIn('jp-example@2026.10.1#jp-example.shares', previous)
        self.assertIn('lifecycle.yaml', seen)
        self.assertIn('2 case(s) of jp-example@2026.10.2 hold', notes[0])

    def test_changed_result_fails_unless_declared(self):
        self.manifest('2026.11.1')
        notes, errors, _ = self.check(failing={'carries the basis'})
        self.assertEqual(len(errors), 1)
        self.assertIn("case 'carries the basis'", errors[0])
        self.assertIn("versions: ['2026.10.2']", errors[0])
        self.manifest('2026.11.1', "fixes:\n  - versions: ['2026.10.2']\n    cases: ['carries the basis']\n"
                                   "    message: {en: corrected, ja: 訂正}\n")
        notes, errors, _ = self.check(failing={'carries the basis'})
        self.assertEqual(errors, [])
        self.assertIn('1 declared fix', notes[0])

    def test_fix_for_another_release_does_not_excuse_a_change(self):
        self.manifest('2026.11.1', "fixes:\n  - versions: ['2026.9.1']\n    cases: ['carries the basis']\n"
                                   "    message: {en: corrected, ja: 訂正}\n")
        _, errors, _ = self.check(failing={'carries the basis'})
        self.assertEqual(len(errors), 1)

    def test_stale_or_unknown_declarations_fail(self):
        self.manifest('2026.11.1', "fixes:\n  - versions: ['2026.10.2']\n    cases: ['carries the basis', 'no such case']\n"
                                   "    message: {en: corrected, ja: 訂正}\n")
        _, errors, _ = self.check()
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("'no such case'" in e and 'does not have' in e for e in errors))
        self.assertTrue(any("'carries the basis'" in e and 'unchanged' in e for e in errors))

    def test_compares_with_the_highest_release(self):
        self.release('2026.10.10', SUITE.replace('2026.10.2#', '2026.10.10#'))
        self.manifest('2026.11.1')
        notes, errors, seen = self.check()
        self.assertEqual(errors, [])
        self.assertIn('of jp-example@2026.10.10 hold', notes[0])
        self.assertIn('jp-example@2026.11.1#', seen['previous-release.lifecycle.yaml'])


if __name__ == '__main__':
    unittest.main()
