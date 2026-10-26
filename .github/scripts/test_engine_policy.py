"""Published-engine policy and real-signature download regressions."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('engine_policy', SCRIPTS / 'check-engine.py')
POLICY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(POLICY)


class Policy(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / '.github').mkdir()
        (self.root / 'JP/jp-example').mkdir(parents=True)
        self.pin = self.root / '.github/engine.txt'
        self.pin.write_text('version v0.2.18\nbindings 5\n')
        self.manifest = self.root / 'JP/jp-example/overlay.yaml'
        self.manifest.write_text('requires_bindings: 5\n')

    def test_stable_pin_and_compatible_packages(self):
        version, bindings = POLICY.read_pin(self.root)
        self.assertEqual((version, bindings), ('v0.2.18', 5))
        POLICY.check_packages(self.root, bindings)

    def test_candidate_urls_prereleases_and_ambiguous_pins_refuse(self):
        for pin in ['version main\nbindings 5', 'version v0.2.20-rc1\nbindings 5',
                    'version https://example.com/iris\nbindings 5', 'version v0.2.18\nbindings 0',
                    'version v0.2.18\nversion v0.2.19\nbindings 5',
                    'version v0.2.18\nbindings 5\nsource candidate', 'version v0.2.18']:
            with self.subTest(pin=pin), self.assertRaises(ValueError):
                self.pin.write_text(pin)
                POLICY.read_pin(self.root)

    def test_newer_missing_or_duplicate_requirements_refuse(self):
        for text in ['requires_bindings: 6\n', '', 'requires_bindings: 5\nrequires_bindings: 5\n']:
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'Release the core capability first'):
                self.manifest.write_text(text)
                POLICY.check_packages(self.root, 5)

    def test_root_and_regional_packages_are_checked(self):
        (self.root / 'common').mkdir()
        (self.root / 'common/overlay.yaml').write_text('requires_bindings: 6\n')
        with self.assertRaisesRegex(ValueError, 'common/overlay.yaml'):
            POLICY.check_packages(self.root, 5)

    def test_only_published_stable_release_metadata_passes(self):
        release = dict(tag_name='v0.2.18', draft=False, prerelease=False, published_at='2026-10-24T00:00:00Z')
        POLICY.check_release(release, 'v0.2.18')
        for change in [dict(tag_name='v0.2.19'), dict(draft=True), dict(prerelease=True),
                       dict(published_at=None), dict(draft=None), dict(prerelease=None)]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                POLICY.check_release({**release, **change}, 'v0.2.18')

    def test_candidate_override_refuses_before_execution(self):
        result = subprocess.run(['bash', str(SCRIPTS / 'run-goldens.sh'), '--bindings', '6'],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('overrides are forbidden', result.stderr + result.stdout)


@unittest.skipUnless(shutil.which('minisign'), 'minisign required for real signature checks')
class Download(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        scripts = self.root / 'repo/.github/scripts'
        scripts.mkdir(parents=True)
        for name in ['check-engine.py', 'fetch-iris.sh']:
            shutil.copy2(SCRIPTS / name, scripts / name)
        (scripts.parent / 'engine.txt').write_text('version v0.2.18\nbindings 5\n')
        package = scripts.parents[1] / 'sample'
        package.mkdir()
        (package / 'overlay.yaml').write_text('requires_bindings: 5\n')
        self.script = scripts / 'fetch-iris.sh'
        self.assets = self.root / 'assets'
        self.assets.mkdir()
        self.binary = self.assets / 'iris_linux_amd64'
        self.binary.write_text('#!/bin/sh\necho "iris v0.2.18"\n')
        (self.assets / 'version.txt').write_text('v0.2.18\n')
        (self.assets / 'release-state.json').write_text(json.dumps(dict(tag_name='v0.2.18', draft=False,
            prerelease=False, published_at='2026-10-24T00:00:00Z')))
        key, pub = self.root / 'key', self.root / 'pub'
        subprocess.run(['minisign', '-G', '-W', '-s', str(key), '-p', str(pub)], capture_output=True, check=True)
        import hashlib
        (self.assets / 'checksums.txt').write_text(''.join(
            f'{hashlib.sha256((self.assets / name).read_bytes()).hexdigest()}  {name}\n'
            for name in ['iris_linux_amd64', 'version.txt']))
        subprocess.run(['minisign', '-S', '-s', str(key), '-m', str(self.assets / 'checksums.txt')],
                       capture_output=True, check=True)
        text = self.script.read_text()
        self.script.write_text(text.replace('RWRln0tEJszZEcTL7VcSL5XR+zcAA2FyqnfOAeLDnwaE7LAa7E3tJCCJ',
                                            pub.read_text().splitlines()[-1]))
        bin_dir = self.root / 'bin'
        bin_dir.mkdir()
        curl = bin_dir / 'curl'
        curl.write_text('''#!/usr/bin/env python3
import os, pathlib, shutil, sys
args=sys.argv[1:]
source = 'release-state.json' if '/releases/tags/' in args[-1] else args[-1].rsplit('/', 1)[-1]
if os.environ.get('MISSING_RELEASE') and source == 'release-state.json': sys.exit(22)
shutil.copyfile(pathlib.Path(os.environ['ASSETS']) / source, args[args.index('-o')+1])
''')
        curl.chmod(0o755)
        self.env = {**os.environ, 'PATH': str(bin_dir) + os.pathsep + os.environ['PATH'],
                    'ASSETS': str(self.assets), 'RUNNER_TEMP': str(self.root / 'runtime'),
                    'GITHUB_PATH': str(self.root / 'github-path')}

    def fetch(self, **env):
        return subprocess.run(['bash', str(self.script)], env={**self.env, **env},
                              capture_output=True, text=True)

    def test_download_requires_real_signature_hash_and_version(self):
        result = self.fetch()
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertTrue((Path(self.env['RUNNER_TEMP']) / 'iris/iris').is_file())
        self.binary.write_text('tampered')
        result = self.fetch()
        self.assertNotEqual(result.returncode, 0)

    def test_missing_draft_and_prerelease_engines_refuse(self):
        self.assertNotEqual(self.fetch(MISSING_RELEASE='1').returncode, 0)
        metadata = self.assets / 'release-state.json'
        original = json.loads(metadata.read_text())
        for change in [dict(draft=True), dict(prerelease=True), dict(published_at=None)]:
            metadata.write_text(json.dumps({**original, **change}))
            result = self.fetch()
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('already published', result.stderr + result.stdout)

    def test_bad_signature_refuses(self):
        (self.assets / 'checksums.txt.minisig').write_text('not a signature')
        self.assertNotEqual(self.fetch().returncode, 0)


if __name__ == '__main__':
    unittest.main()
