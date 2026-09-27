# Contributing

**English** | [日本語](CONTRIBUTING.ja.md)

Thank you for improving the rules IrisBooks books are checked against. Every
change here reaches every book that upgrades to the next version, so the bar is
a reviewer being able to see exactly which figures change and why.

## What belongs in an overlay

- **Method, not rates.** A rule's structure, a recipe's steps, rounding, the
  order of a computation — yes. A rate table that a tax reform can change
  without changing the method — no; make it a recipe parameter.
- **Only what a book records.** Rules see the book's own files (`book`,
  `journal`, `line`, `asset`, `assets`); they cannot fetch anything.
- **Both languages.** Every rule message has `en` and `ja`.

## Every pull request

1. **Golden tests.** Add or update cases under `<id>/tests/` for each rule,
   recipe or derivation you change, then run `iris overlay test --dir <id>`
   (`iris` v0.2.0 or later). CI runs the same suites.
2. **Version.** If anything outside `<id>/tests/` changed since the last
   `<id>@…` tag, bump `version` in `<id>/overlay.yaml` (`YYYY.MM.N`, higher
   than the last tag). Several PRs may land under one new version before it is
   released. CI checks this (`.github/scripts/check-versions.sh`).
3. **Sign-off.** Sign each commit with the
   [Developer Certificate of Origin](https://developercertificate.org/):
   `git commit -s`. The sign-off must match the commit author. By signing off
   you certify you may contribute the change under the Apache License 2.0.

## Bindings — what a rule can see

The functions and values CEL can use are provided by the `iris` engine, which is
not in this repository. An overlay declares the bindings version it needs
(`requires_bindings` in `overlay.yaml`); CI loads it with the latest released
`iris`, so an overlay can only use bindings that have already shipped. If you
need a new one, open an issue first — the engine change ships in an `iris`
release before the overlay that uses it can merge.

## From a book layer to a pull request

A book layer (`config/overlays/`) declares `extends: <id>@<version>` and holds
only additions and overrides. To upstream it, move its files into the matching
`<id>/` directories here (a rule with the same `id` replaces the published
one), drop `extends:`, bring its tests along, and bump the version.

## Review and release

A maintainer reviews every pull request (see `.github/CODEOWNERS`). Released
versions are tags `<id>@<version>`, made by a maintainer after merge; an `iris`
release embeds the overlays tagged at the time.
