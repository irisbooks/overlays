#!/usr/bin/env bash
# Every overlay whose content outside tests/ changed since its last released
# tag (<id>@<version>) must declare a new, higher version in <id>/overlay.yaml.
# A released version never changes: books record it as the source of the
# figures a recipe computed, and iris re-runs the recipe under it.
# Needs the tags: in CI, check out with fetch-depth: 0.
set -euo pipefail

fail=0
for manifest in */overlay.yaml; do
  id="${manifest%/overlay.yaml}"
  declared="$(sed -n 's/^id: *//p' "$manifest")"
  version="$(sed -n 's/^version: *//p' "$manifest")"
  if [ "$declared" != "$id" ]; then
    echo "::error file=$manifest::id '$declared' does not match its directory '$id'"
    fail=1
  fi
  if ! [[ "$version" =~ ^[0-9]{4}\.[0-9]{2}\.[0-9]+$ ]]; then
    echo "::error file=$manifest::version '$version' is not YYYY.MM.N"
    fail=1
    continue
  fi
  last="$(git tag -l "$id@*" | sed "s/^$id@//" | sort -V | tail -1)"
  if [ -z "$last" ]; then
    echo "$id@$version: not released yet"
  elif [ "$version" = "$last" ]; then
    if git diff --quiet "$id@$last" -- "$id" ":(exclude)$id/tests"; then
      echo "$id@$version: unchanged since its tag"
    else
      echo "::error file=$manifest::$id changed outside tests/ since $id@$last — bump version"
      git diff --stat "$id@$last" -- "$id" ":(exclude)$id/tests"
      fail=1
    fi
  elif [ "$(printf '%s\n%s\n' "$last" "$version" | sort -V | tail -1)" != "$version" ]; then
    echo "::error file=$manifest::version $version is lower than the released $id@$last"
    fail=1
  else
    echo "$id@$version: new version (last released: $id@$last)"
  fi
done
exit "$fail"
