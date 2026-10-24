# Calculate consumption-tax supporting figures

**English** | [日本語](README.ja.md)

Calculates supporting figures from posted, classified journal lines using either
general or simplified taxation. Preview a recipe, then explicitly save the
reviewed result under `filings/` with its calculation provenance.

## Before use

Requires [jp-tax-classification@2026.10.1](../jp-tax-classification/README.md),
but not `jp-tax-amount`. Read the guide before setting `scope_confirmed: true`.
Coverage is limited to the documented 10%/8% calculations; the result is a
calculation aid. Statutory return preparation and submission are separate work.

See [availability and engine requirements](../../README.md#choose-a-package) and
[package installation and selection](../../README.md#use-packages-in-a-book).

## Follow the task

Task ID: `jp-tax-filing.filing`. From the Book folder:

```sh
iris context --task jp-tax-filing.filing
iris overlay guide jp-tax-filing.filing
```

Read the [workflow guide](guides/filing.md) for inputs, commands and coverage.
The [task definition](tasks.yaml) links these executable examples:

- [Calculation examples](tests/filings.yaml)
- [Scope confirmation examples](tests/coverage.yaml)
- [Transition-period examples](tests/transitions.yaml)
