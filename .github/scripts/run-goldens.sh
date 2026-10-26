#!/usr/bin/env bash
# Run every package's golden suites with the `iris` on PATH.
#
# Uses only the signed, published engine installed by fetch-iris.sh.
# The pin is the compatibility baseline even when a newer engine is being built.
set -euo pipefail

[ "$#" -eq 0 ] || { echo "::error::candidate/bindings overrides are forbidden; publish and pin the core first"; exit 1; }
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
version="$(python3 "$SCRIPT_DIR/check-engine.py" --version)"
[ "$(iris version)" = "iris $version" ] || { echo "::error::run golden tests with the verified published engine $version"; exit 1; }

if ! iris overlay test -h 2>&1 | grep -q 'overlay-dir'; then
  echo "::error::$(iris version) lacks overlay test --dir; pin a compatible signed engine"
  exit 1
fi

shopt -s nullglob
manifests=(*/overlay.yaml */*/overlay.yaml)
[ "${#manifests[@]}" -gt 0 ] || { echo "::error::no overlay packages found"; exit 1; }
status=0
for manifest in "${manifests[@]}"; do
  package_dir="${manifest%/overlay.yaml}"
  echo "::group::$package_dir"
  iris overlay test --dir "$package_dir" || status=1
  echo "::endgroup::"
done
exit "$status"
