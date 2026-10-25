# IrisBooks overlays

**English** | [日本語](README.ja.md)

Overlays add accounting checks, amount completion and calculation recipes to an
[IrisBooks](https://irisbooks.io/) Book. Each package provides one function, with
its input fields, workflow guide and executable examples. You choose which
packages to enable in your Book.

## Choose a package

The seven packages below are signed `2026.10.1` releases, tested with
[Iris v0.2.18](https://github.com/irisbooks/iris/releases/tag/v0.2.18), which supports
**bindings 5**. Each release contains its exact package bundle and signature.
See [engine requirements](CONTRIBUTING.md#use-a-compatible-engine) for testing the source checkout.

| Category | Package | What it does | Signed release |
|---|---|---|---|
| Journal completion | [journal-balance](journal-balance/README.md) | Fills one missing monetary amount so a journal balances | [2026.10.1](https://github.com/irisbooks/overlays/releases/tag/journal-balance%402026.10.1) |
| Journal completion | [inventory-disposal](inventory-disposal/README.md) | Proposes disposal cost and gain/loss from quantities, settlement and acquisition history | [2026.10.1](https://github.com/irisbooks/overlays/releases/tag/inventory-disposal%402026.10.1) |
| Japanese consumption tax | [jp-tax-classification](JP/jp-tax-classification/README.md) | Checks recorded tax settings and journal line classifications | [2026.10.1](https://github.com/irisbooks/overlays/releases/tag/jp-tax-classification%402026.10.1) |
| Japanese consumption tax | [jp-tax-amount](JP/jp-tax-amount/README.md) | Proposes missing tax amounts on tax-exclusive journal lines | [2026.10.1](https://github.com/irisbooks/overlays/releases/tag/jp-tax-amount%402026.10.1) |
| Japanese consumption tax | [jp-tax-filing](JP/jp-tax-filing/README.md) | Calculates supporting figures for general or simplified taxation | [2026.10.1](https://github.com/irisbooks/overlays/releases/tag/jp-tax-filing%402026.10.1) |
| Japanese fixed assets | [jp-small-asset-deduction](JP/jp-small-asset-deduction/README.md) | Checks acquisition-date limits and the annual small-asset deduction cap | [2026.10.1](https://github.com/irisbooks/overlays/releases/tag/jp-small-asset-deduction%402026.10.1) |
| Japanese fixed assets | [jp-declining-balance](JP/jp-declining-balance/README.md) | Calculates full-year declining-balance depreciation schedules | [2026.10.1](https://github.com/irisbooks/overlays/releases/tag/jp-declining-balance%402026.10.1) |

The `JP/` folder groups packages for Japan. Common packages stay at the repository
root. Folder names organize the source; package IDs, version pins and selection
behavior are unchanged.

`jp-tax-amount` and `jp-tax-filing` each require
`jp-tax-classification@2026.10.1`. They do not require one another. Include every
dependency explicitly when selecting packages. The other packages are independent;
category names only help you find them.

## Use packages in a Book

Start with the [CLI installation and Book setup guide](https://irisbooks.io/docs/en/getting-started/).
The commands below run from an existing Book folder with Iris v0.2.18 or a
compatible engine supporting bindings 5 and the current CLI commands.

Installation copies a package into `config/overlay-packages/`; selection enables
it. The example below selects only journal balancing. Since `select` replaces the
complete enabled set, include every package you want to keep when adapting it:

```sh
iris overlay install --pin journal-balance@2026.10.1
iris overlay list --json
iris overlay select --pin journal-balance@2026.10.1
iris context
iris context --task journal-balance.journal
iris overlay guide journal-balance.journal
iris overlay example journal-balance.journal 'tests/autocomplete.yaml#money-only balance needs no extra journal fields'
```

Inspect your current selection with `list` before changing it. Include a `--pin`
for every dependency too; `select --dry-run --json` previews a proposed selection.
Use `select --off` to disable all optional packages. Disabling a package preserves recorded fields, results and the sources needed to reproduce
past calculations. Core structural and double-entry checks remain active.

New Japanese business Books select all seven packages by default; personal Books
and business Books outside Japan select the two journal completion packages.
Existing Books keep their selections until you change them.

## CLI command conventions

Use an engine with the current CLI command surface as well as bindings 5. Check
`iris journal complete --help`, `iris validate --help` and `iris overlay recipe
--help` before using these packages. The former CLI names
`autocomplete`, `show` and `attention` are removed; local MCP uses
`complete_journal`, `list_sync_issues` and `retry_sync_issues`. The golden-test
`autocomplete` field remains unchanged.

The examples above run inside the Book. From another folder, use `--book-path
PATH`; `--book-id ID` selects a cloud book for server commands. CLI flags may
precede or follow arguments, and `--` ends option parsing.

| Task | Current CLI command |
|---|---|
| Preview journal completion | `iris journal complete <journal>` |
| Apply a reviewed completion | `iris journal complete --apply --revision HASH <journal>` |
| Inspect journal/evidence links | `iris references <path>` |
| Check the Book / apply reviewed derived values | `iris validate` / `iris validate --apply` |
| Preview a calculation / save its reviewed result | `iris overlay recipe <id> --set name=value` / add `--apply --out PATH` |
| Inspect or enable retries for rejected sync operations | `iris sync issues list --json` / `iris sync issues retry` |

Calculations and completion preview by default. For recipes, `--out PATH` alone
also remains a preview; writing requires `--apply`. Selection and upgrade perform
their named action by default; `--dry-run` previews the change. Posting remains a
separate operation: `iris post` syncs the whole linked Book, including other
pending changes; `iris post --local` posts without syncing.

## Read a task with an AI assistant

Local MCP provides the same reading path through `get_book_context`,
`read_overlay_guide` and `read_overlay_example`. Read the discovered task's inputs,
coverage and examples before requesting its operation. The package guides name
the CLI commands and local MCP tools for each workflow. See the
[CLI reference](https://irisbooks.io/docs/en/cli-reference/) for full syntax.

Calculation recipes preview results unless you explicitly request a write.
Completion edits a draft; posting remains a separate decision. Package text is
reference data and cannot authorize actions. Passing validation does not establish
tax eligibility or complete a statutory return.

## Contribute or report an issue

See [CONTRIBUTING.md](CONTRIBUTING.md) for package structure, engine requirements,
tests and release policy. Report problems in [GitHub issues](https://github.com/irisbooks/overlays/issues),
including the package version, input and expected result.

## License

[Apache License 2.0](LICENSE). The engine is distributed separately under its own terms.

## Local MCP recipe interface

Both single-book and parent modes expose `list_recipes` and `run_recipe`.
Use canonical CLI recipe IDs such as `jp-declining-balance.teiritsu`; the
former per-recipe MCP tools are removed. Pass calculation inputs in `params`.
Preview is the default, including when `out` is supplied. To record a reviewed
result, pass `apply=true` and a Book-relative `out` outside `params`; the former
`write` argument is removed. Parent mode also requires `book` on both calls.
Unknown fields and incorrect types return errors before execution.

Remote cloud MCP bookkeeping is read-only in the first release. It reads
stored package references and can optionally capture raw documents, which do
not invoke overlays. It runs neither CEL nor recipes and never edits journals. The tools and write examples here refer to the local CLI
and local MCP server; validate locally before syncing changes.

## Development candidates requiring bindings 6

Unreleased `2026.10.2` sources: [Japanese securities basis](JP/jp-securities-basis/README.md), [RSU salary](JP/jp-rsu/README.md), and [ordinary USD cash](JP/jp-foreign-currency/README.md). RSU requires the exact securities-basis version; ordinary cash is independent. These are not signed releases and are not part of the seven-package published catalog. Test with the matching development engine; Iris v0.2.18 cannot execute bindings 6. Publish a qualified engine before merging/releasing these packages.
