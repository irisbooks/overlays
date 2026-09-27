#!/usr/bin/env bash
# Every non-merge commit in base..head carries a Developer Certificate of
# Origin sign-off matching its author (git commit -s).
# https://developercertificate.org/
set -euo pipefail

base="${1:?usage: check-dco.sh <base-sha> <head-sha>}"
head="${2:?usage: check-dco.sh <base-sha> <head-sha>}"
fail=0
for c in $(git rev-list --no-merges "$base..$head"); do
  author="$(git show -s --format='%an <%ae>' "$c")"
  if ! git show -s --format='%(trailers:key=Signed-off-by,valueonly)' "$c" | grep -qxF "$author"; then
    echo "::error::$(git show -s --format='%h %s' "$c") — missing 'Signed-off-by: $author' (amend with git commit -s)"
    fail=1
  fi
done
exit "$fail"
