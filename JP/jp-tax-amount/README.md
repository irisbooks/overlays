# Propose a missing consumption-tax amount

**English** | [日本語](README.ja.md)

Proposes a missing `line.tax.amount` on a classified tax-exclusive journal line.
It calculates net amount × rate / 100 and truncates fractional yen.

## Before use

Requires [jp-tax-classification@2026.10.1](../jp-tax-classification/README.md).
Tax-inclusive Books receive no proposal, and existing amounts are preserved.
Review invoice rounding before applying. The proposal does not create a separate
tax posting. The filing package is optional.

See [availability and engine requirements](../../README.md#choose-a-package) and
[package installation and selection](../../README.md#use-packages-in-a-book).

## Follow the task

Task ID: `jp-tax-amount.propose`. From the Book folder:

```sh
iris context --task jp-tax-amount.propose
iris overlay guide jp-tax-amount.amount
```

Read the [workflow guide](guides/amount.md) for inputs, commands and coverage.
The [task definition](tasks.yaml) links these executable examples:

- [Proposal and preserved-value examples](tests/amount.yaml)
