# Contributing

**English** | [日本語](CONTRIBUTING.ja.md)

Thank you for improving the rules IrisBooks books are checked against. Every
change here reaches every book that upgrades to the next version, so the bar is
a reviewer being able to see exactly which figures change and why.

## What belongs in an overlay

- **Method, and statutory figures dated and cited.** A rule's structure, a
  recipe's steps, rounding, the order of a computation — yes. A rate, threshold
  or percentage fixed by law may live here too, as a named function in
  `functions.yaml` (`shoutoku_max` and `non_invoice_periods` are examples):
  key it on the date the law keys it on, cite the provision or the NTA page in
  its `doc`, and past a 適用期限 return what the law then provides (usually
  nothing), not the last figure. A reform changes a figure in a new version;
  the figures for earlier dates stay. Figures that differ by taxpayer or by
  municipality stay recipe parameters. Some recipes still take statutory
  figures as parameters (the 定率法 rates, the みなし仕入率); moving them here
  is welcome.
- **Only what a book records.** Rules see the book's own files (`book`,
  `journal`, `line`, `asset`, `assets`); they cannot fetch anything.
- **Both languages.** Every rule message has `en` and `ja`.

## Every pull request

1. **Golden tests.** Add or update cases under `<id>/tests/` for each rule,
   recipe, derivation or journal completion you change, then run `iris overlay test --dir <id>`
   (`iris` v0.2.0 or later). CI runs the same suites.
2. **Version.** If anything outside `<id>/tests/` changed since the last
   `<id>@…` tag, bump `version` in `<id>/overlay.yaml` (`YYYY.MM.N`, higher
   than the last tag). Several PRs may land under one new version before it is
   released. CI checks this (`.github/scripts/check-versions.sh`).
3. **Sign-off.** Sign each commit with the
   [Developer Certificate of Origin](https://developercertificate.org/):
   `git commit -s`. The sign-off must match the commit author. By signing off
   you certify you may contribute the change under the Apache License 2.0.

Journal completion golden cases use the `autocomplete` block with `chart`,
`journal` and optional `history`. Supply complete expected `lines` in journal
syntax, or an `error` substring. See `default/tests/autocomplete.yaml`.
These cases require a binding-v3 engine; they must not be silently skipped by
an older engine.

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
