#!/usr/bin/env python3
"""Require a stable published-engine pin and compatible package manifests."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
STABLE = re.compile(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")


def read_pin(root):
    fields = {}
    for line in (root / ".github/engine.txt").read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 2 or parts[0] not in ("version", "bindings") or parts[0] in fields:
            raise ValueError("engine.txt must contain exactly one version and one bindings value")
        fields[parts[0]] = parts[1]
    if not STABLE.fullmatch(fields.get("version", "")):
        raise ValueError("engine pin must be a stable vX.Y.Z; unpublished commits, URLs and prereleases are forbidden")
    if not re.fullmatch(r"[1-9][0-9]{0,2}", fields.get("bindings", "")):
        raise ValueError("engine pin bindings must be a positive integer")
    return fields["version"], int(fields["bindings"])


def check_packages(root, bindings):
    manifests = sorted([*root.glob("*/overlay.yaml"), *root.glob("*/*/overlay.yaml")])
    if not manifests:
        raise ValueError("no overlay packages found")
    for manifest in manifests:
        values = re.findall(r"^requires_bindings:[ \t]*([1-9][0-9]{0,2})[ \t]*(?:#.*)?$", manifest.read_text(), re.M)
        if len(values) != 1 or int(values[0]) > bindings:
            raise ValueError(f"{manifest.relative_to(root)} requires bindings {values[0] if len(values) == 1 else '?'}; "
                             f"the published engine pin provides {bindings}. Release the core capability first, "
                             "then update engine.txt and this package. Do not use an unpublished engine.")


def check_release(release, version):
    if (release.get("tag_name") != version or release.get("draft") is not False
            or release.get("prerelease") is not False or not release.get("published_at")):
        raise ValueError(f"{version} must be an already published, non-draft stable engine release")


def main(args):
    version, bindings = read_pin(ROOT)
    check_packages(ROOT, bindings)
    if args == ["--version"]:
        print(version)
    elif len(args) == 2 and args[0] == "--release":
        check_release(json.loads(Path(args[1]).read_text()), version)
        print(f"Published engine policy passed: {version}, bindings {bindings}")
    elif not args:
        print(f"Engine requirements passed: {version}, bindings {bindings}; publication and signatures checked during download")
    else:
        raise ValueError("usage: check-engine.py [--version | --release metadata.json]")


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except (ValueError, OSError) as error:
        sys.exit(f"::error::{error}")
