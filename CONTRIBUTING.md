# Contributing

**English** | [日本語](CONTRIBUTING.ja.md)

Contributions can improve checks, completion, calculations and documentation.
Explain which inputs or figures change and why, so a reviewer can reproduce the
result. For questions or proposed engine changes, open a
[GitHub issue](https://github.com/irisbooks/overlays/issues).

## Use a compatible engine

The published `2026.10.1` packages all declare `requires_bindings: 5`.
Bindings are the functions and values the Iris engine makes available to package
expressions written in CEL. The engine is distributed separately; start with the
[CLI installation guide](https://irisbooks.io/docs/en/getting-started/) and
[signed engine releases](https://github.com/irisbooks/iris/releases).

[Iris v0.2.18](https://github.com/irisbooks/iris/releases/tag/v0.2.18) supports
bindings 5 and `iris overlay test --dir`; all 59 golden cases for this catalog
pass with that signed engine. For another engine, check its binding and command
support explicitly. CI tests with the signed engine pinned in
[`.github/engine.txt`](.github/engine.txt), so a new engine release never changes
the result for an unchanged commit. Raise the pin in the PR that needs a newer
engine. Unsupported bindings or test suites must fail, never be skipped. Future engine bindings must
ship before a package using them can merge or be released. Published bundles and
signatures are linked from the [package catalog](README.md#choose-a-package).

The guides also require the current command surface: journal completion is
`iris journal complete`, applying derived fields uses `iris validate --apply`,
and recipe writes use `--apply --out PATH`. Verify examples with that engine's
`--help` and update English/Japanese guides plus user-visible YAML descriptions
and messages together. Keep MCP names and examples aligned too: use `complete_journal`, and the shared
`list_recipes` / `run_recipe` interface in both modes. Recipe IDs match the CLI;
`params` contains only recipe inputs. Preview is the default; `apply=true` plus
`out` records a result. Golden-test field names such as `autocomplete` stay unchanged.

From this repository's root, test a package with:

```sh
iris overlay test --dir journal-balance
iris overlay test --dir JP/jp-tax-classification
```

Repeat for each changed package. No Book folder or engine source checkout is
needed for `--dir` tests.

## Published-engine dependency policy

Every package must work with the already published, signed, stable engine pinned
in `.github/engine.txt`. An engine source tag, PR build, staging candidate, draft
release or prerelease does not satisfy this dependency. There is no candidate
engine or `--bindings` override for the merge gate.

CI checks the pin and every package's `requires_bindings`, confirms the GitHub
release is published and stable, verifies its signature and checksums, and runs
all package golden tests with that exact binary. Lowering `requires_bindings`
without adapting the implementation is not a compatibility fix; package loading
and real execution must pass too.

If a package needs a new core primitive, release that engine capability first
with the existing compatible catalog. After publication, update the engine pin
and add the package change. The core release must not wait for the dependent
unpublished package. Merge and tag package source only after this published-engine
gate passes; vendor the tag into the application afterwards. The final application
candidate may repeat tests with its new engine as an additional compatibility
check, but cannot replace the published-engine baseline.

Run the same checks locally:

```sh
python3 .github/scripts/check-engine.py
# In CI, fetch-iris.sh downloads/verifies the pin and puts it on GITHUB_PATH.
# Locally, install that exact signed version and put it on PATH first.
.github/scripts/run-goldens.sh
```

## Decide what belongs in a layer or core

- **Put policy and supported calculations in Overlays.** Regional eligibility,
  dated legal values, classifications, rounding choices and recipes belong here.
  Try clear, exact, bounded CEL functions on the published engine before asking
  for a native primitive. Complexity or reuse alone does not make a function core.
- **Keep core guarantees universal.** Book structure, double-entry integrity,
  exact native types, execution budgets and guarded host operations must hold
  with every optional package disabled. Core may expose a typed fact snapshot,
  general arithmetic/recurrence primitive or checked posting proposal; the layer
  chooses the regional method and treatment.
- **Separate policy from facts and local adaptations.** Observed prices/rates,
  source evidence and owner settings are Book data. A business-specific override
  belongs in a trusted Book-local layer with exact parents and retained source.
  Select independent functions and declare necessary exact dependencies; a
  dependency does not expose another package's private CEL helpers.
- **Separate calculation from apply.** A recipe computes figures/proposals. An
  authorized host operation applies changes with scope, revision and lock guards.
  CEL cannot fetch facts, access credentials or perform arbitrary I/O. Package
  instructions alone do not authorize actions.
- **Require evidence for an engine addition.** Show the smallest attempted case
  on the published engine, the missing data/numeric/apply/state capability, and
  the minimal jurisdiction-independent interface. Specify bounds, refusal and
  replay/compatibility tests. Avoid both premature native code and an opaque CEL
  workaround. Report missing behavior explicitly rather than silently narrowing
  the feature or skipping tests.
- **Publish the core prerequisite first.** Follow the dependency policy above;
  the core capability release must work with existing compatible packages and
  must not wait for its unpublished consumer.

For example, [RSU valuation functions](JP/jp-rsu/functions.yaml) calculate exact
price × FX values on published bindings 5, with
[golden cases](JP/jp-rsu/tests/valuation.yaml) and an
[independent rational oracle](.github/scripts/check-rsu-valuation.py). The
[workflow guide](JP/jp-rsu/guides/vesting.md) separately identifies the existing
posting-apply and inventory-state limits. Arithmetic alone did not require a new
engine API. These are ordinary code-review criteria, not another release approval.

## Keep each package focused

An overlay provides one independently useful accounting function. Keep its
fields, checks, calculations, guide and examples together. Declare exact
`requires_overlays` versions for necessary dependencies; users must select those
dependencies explicitly. Shared helper code alone does not justify enabling
unrelated behavior.

- **Date and cite statutory figures.** Put rates or thresholds in named
  `functions.yaml` functions when appropriate. Use the date specified by the law,
  cite the provision or NTA page in `doc`, and encode what applies after expiry.
  Keep earlier dates' figures when adding a reform in a new version. Values that
  depend on the taxpayer or municipality remain recipe parameters. See
  [shoutoku_max](JP/jp-small-asset-deduction/functions.yaml) and
  [non_invoice_periods](JP/jp-tax-filing/functions.yaml).
- **Use recorded inputs.** Expressions read the Book's own data (`book`,
  `journal`, `line`, `asset`, `assets`); they cannot fetch external facts.
- **Keep both reading paths usable.** Provide `en` and `ja` messages and recipe
  or completion descriptions. Update the English and Japanese README and guide
  together when behavior, inputs or coverage change.

## Find the file to change

Common packages live at `<id>/`; regional packages live at `<region>/<id>/`.
Region folder names must use uppercase [ISO 3166-1 alpha-2](https://www.iso.org/iso-3166-country-codes.html)
country or territory codes, such as `JP`, `US` and `GB`.

Regional overlay IDs must start with the corresponding lowercase region code
and a hyphen: `jp-` for `JP`, for example `JP/jp-tax-amount/`.

The paths below are relative to a package directory. Use that directory with
`--dir`. The manifest ID and release tag do not include the region folder path.

| File | Purpose |
|---|---|
| `overlay.yaml` | Package ID, version, required bindings and exact dependencies |
| `fields.yaml` | Input types, requiredness, choices and descriptions |
| `functions.yaml` | Named CEL helpers and source citations |
| `rules/*.yaml` | Validation conditions, assertions and localized messages |
| `derive/*.yaml` | Missing-field proposals |
| `completions/*.yaml` | Journal completion definitions |
| `recipes/*.yaml` | Calculation parameters, steps and result shape |
| `tasks.yaml` | Task IDs, inputs, operations, guide and executable example selectors |
| `guides/*.md` | Workflow, coverage and remaining human judgment |
| `tests/*.yaml` | Inputs with expected results or errors (golden tests) |

Only include files the function needs. Start with the matching package in the
[catalog](README.md#choose-a-package). For Book-local definitions and configuration,
see the [format reference](https://irisbooks.io/docs/en/book-format-reference/).
English guide names remain the task's canonical reference; a sibling `*.ja.md`
guide is discoverable with a `.ja` suffix, such as `journal-balance.journal.ja`.

## Before opening a pull request

1. **Run golden tests.** Add or update cases for each changed rule, recipe,
   derivation or completion, then run `iris overlay test --dir <package-dir>` with the
   compatible engine described above. For documentation changes, check links and
   run the suite too: guides and task references are loaded as package data.
2. **Check the version.** If files outside `<package-dir>/tests/` changed since the last
   `<id>@…` release tag, increase `version` in `overlay.yaml` (`YYYY.MM.N`). Several
   PRs may share one candidate version before release. Released versions never
   change. Run `.github/scripts/check-versions.sh` with release tags available.
3. **Add a DCO sign-off.** Each commit needs a
   [Developer Certificate of Origin](https://developercertificate.org/) sign-off
   matching its author (`git commit -s`). This certifies your right to contribute
   under Apache License 2.0.

Completion cases use an `autocomplete` block with `chart`, `journal` and optional
`history`. Expect complete journal `lines` or an `error` substring. See
[balancing examples](journal-balance/tests/autocomplete.yaml) and
[disposal examples](inventory-disposal/tests/autocomplete.yaml).

## Contribute a Book-local definition

A Book-local layer in `config/overlays/` declares `extends` with its parent pin or
complete list of parent pins. Copy the relevant additions or overrides into the
matching package here, remove the local `extends` declaration and retain the
package's own manifest. A rule with the same ID replaces that package's rule.
Bring the tests, update both language guides and check the version.

## Review and release

A maintainer reviews every PR; see [CODEOWNERS](.github/CODEOWNERS). After merge,
maintainers tag `<id>@<version>` and publish a signed package bundle. Candidate
bundle building and signing belong to the maintainer's engine release workflow.
An Iris release includes a curated catalog for offline installation. Books keep
exact installed definitions for execution and historical replay.
