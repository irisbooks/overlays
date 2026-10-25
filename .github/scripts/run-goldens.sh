#!/usr/bin/env bash
# Run every package's golden suites with the `iris` on PATH.
#
#   .github/scripts/run-goldens.sh [--bindings N]
#
# N is the binding version the engine provides: by default the pin in
# .github/engine.txt; release qualification passes the candidate engine's
# value. Packages needing more fail here with a clear message — missing
# support is a release blocker, never a skipped success. Run from the
# repository root.
set -euo pipefail

bindings=""
case "${1:-}" in
  --bindings) bindings="${2:?--bindings needs a value}" ;;
  "") bindings="$(awk '$1 == "bindings" {print $2}' .github/engine.txt)" ;;
  *) echo "usage: $0 [--bindings N]" >&2; exit 2 ;;
esac
[[ "$bindings" =~ ^[1-9][0-9]*$ ]] || { echo "::error::engine bindings '$bindings' is not a positive integer"; exit 1; }

if ! iris overlay test -h 2>&1 | grep -q 'overlay-dir'; then
  echo "::error::$(iris version) lacks overlay test --dir; pin a compatible signed engine"
  exit 1
fi

shopt -s nullglob
manifests=(*/overlay.yaml */*/overlay.yaml)
[ "${#manifests[@]}" -gt 0 ] || { echo "::error::no overlay packages found"; exit 1; }
status=0
for manifest in "${manifests[@]}"; do
  required="$(sed -n 's/^requires_bindings: *\([0-9][0-9]*\) *$/\1/p' "$manifest")"
  if [ -z "$required" ] || [ "$required" -gt "$bindings" ]; then
    echo "::error file=$manifest::requires bindings ${required:-?}; the engine provides $bindings — publish and pin a compatible engine first"
    status=1
  fi
done
[ "$status" -eq 0 ] || exit 1
for manifest in "${manifests[@]}"; do
  package_dir="${manifest%/overlay.yaml}"
  echo "::group::$package_dir"
  iris overlay test --dir "$package_dir" || status=1
  echo "::endgroup::"
done
exit "$status"
