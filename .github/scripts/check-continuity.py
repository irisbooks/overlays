#!/usr/bin/env python3
"""Hold every new package release to its last release's golden results.

A release adds behavior and never changes a result an earlier release
produced: Books carry state and saved results across releases, and iris
continues them by package ID. For each package whose version is not tagged
yet, this runs the last release's tests/ against the candidate, with the
package's own `<id>@<version>` inside recorded labels updated to the
candidate. A case that no longer passes must be named by a `fixes` entry in
the candidate's overlay.yaml whose `versions` include that release.

Needs the release tags (check out with fetch-depth: 0), PyYAML and the
verified published iris on PATH (see fetch-iris.sh).
"""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
VERSION = re.compile(r"[0-9]{4}\.[0-9]{2}\.[0-9]+")
# Copies of the last release's suites keep their own file names behind this
# prefix, next to the candidate's suites, so task references still resolve.
PREFIX = "previous-release."


def version_key(version):
    return tuple(int(part) for part in version.split("."))


def git(*args, root=ROOT):
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout


def manifest_value(text, key):
    found = re.findall(rf"^{key}:[ \t]*(\S+)[ \t]*(?:#.*)?$", text, re.M)
    if len(found) != 1:
        raise ValueError(f"overlay.yaml must declare one {key}")
    return found[0]


def last_release(package, root=ROOT):
    versions = [tag.split("@", 1)[1] for tag in git("tag", "-l", f"{package}@*", root=root).split()]
    versions = [v for v in versions if VERSION.fullmatch(v)]
    return max(versions, key=version_key) if versions else None


def released_suites(package, version, root=ROOT):
    """The tests/*.yaml of a release, keyed by file name."""
    tag = f"{package}@{version}"
    files = git("ls-tree", "-r", "--name-only", tag, root=root).splitlines()
    manifests = [f for f in files if f == f"{package}/overlay.yaml" or f.endswith(f"/{package}/overlay.yaml")]
    if len(manifests) != 1:
        raise ValueError(f"{tag} does not contain exactly one {package}/overlay.yaml")
    tests = manifests[0][: -len("overlay.yaml")] + "tests/"
    return {f[len(tests):]: git("show", f"{tag}:{f}", root=root)
            for f in files if f.startswith(tests) and f.endswith(".yaml") and "/" not in f[len(tests):]}


def declared_cases(manifest_text, released):
    import yaml  # PyYAML: apt install python3-yaml, or pip install pyyaml

    cases = set()
    for fix in (yaml.safe_load(manifest_text) or {}).get("fixes") or []:
        if released in (fix.get("versions") or []):
            cases.update(fix.get("cases") or [])
    return cases


def run_iris(package_dir):
    proc = subprocess.run(["iris", "overlay", "test", "--json", "--dir", str(package_dir)], capture_output=True, text=True)
    try:
        return json.loads(proc.stdout)["results"]
    except (ValueError, KeyError):
        raise ValueError(f"iris overlay test could not run the candidate: {proc.stderr.strip() or proc.stdout.strip()}")


def check(package_dir, run=run_iris, root=ROOT):
    """Return (notes, errors) for one package directory."""
    text = (package_dir / "overlay.yaml").read_text()
    package, version = manifest_value(text, "id"), manifest_value(text, "version")
    last = last_release(package, root)
    if last is None or last == version:
        return [f"{package}@{version}: no new release to compare"], []
    suites = released_suites(package, last, root)
    if not suites:
        return [f"{package}@{version}: {package}@{last} has no golden cases"], []
    with tempfile.TemporaryDirectory() as tmp:
        candidate = Path(tmp) / package
        shutil.copytree(package_dir, candidate)
        (candidate / "tests").mkdir(exist_ok=True)
        for name, body in suites.items():
            (candidate / "tests" / (PREFIX + name)).write_text(body.replace(f"{package}@{last}", f"{package}@{version}"))
        results = [r for r in run(candidate) if r["suite"].startswith(PREFIX)]
    declared = declared_cases(text, last)
    names = {r["name"] for r in results}
    changed = {r["name"] for r in results if not r["passed"]}
    errors = []
    for r in results:
        if not r["passed"] and r["name"] not in declared:
            detail = "; ".join(r.get("failures") or [])
            errors.append(f"{package}@{version} changes the result of {package}@{last} case "
                          f"'{r['name']}' ({r['suite'][len(PREFIX):]}): {detail}. A release must not change an "
                          f"earlier result. If this corrects it, declare it in overlay.yaml under fixes "
                          f"(versions: ['{last}'], cases: ['{r['name']}']) with an en/ja message.")
    for name in sorted(declared - names):
        errors.append(f"{package}@{version}: fixes names case '{name}', which {package}@{last} does not have")
    for name in sorted((declared & names) - changed):
        errors.append(f"{package}@{version}: fixes names case '{name}', but its {package}@{last} result is unchanged")
    notes = [f"{package}@{version}: {len(results)} case(s) of {package}@{last} hold"
             + (f", {len(declared & changed)} declared fix(es)" if declared & changed else "")]
    return notes, errors


def main(args):
    if args:
        raise ValueError("usage: check-continuity.py")
    version = subprocess.run([sys.executable, str(Path(__file__).with_name("check-engine.py")), "--version"],
                             check=True, capture_output=True, text=True).stdout.strip()
    engine = subprocess.run(["iris", "version"], capture_output=True, text=True).stdout.strip()
    if engine != f"iris {version}":
        raise ValueError(f"run with the verified published engine {version}, not {engine or 'no iris'}")
    manifests = sorted([*ROOT.glob("*/overlay.yaml"), *ROOT.glob("*/*/overlay.yaml")])
    if not manifests:
        raise ValueError("no overlay packages found")
    failed = False
    for manifest in manifests:
        notes, errors = check(manifest.parent)
        for note in notes:
            print(note)
        for error in errors:
            print(f"::error file={manifest.relative_to(ROOT)}::{error}")
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except (ValueError, subprocess.CalledProcessError) as error:
        print(f"::error::{error}")
        sys.exit(1)
