# Check consumption-tax classifications

**English** | [日本語](README.ja.md)

Checks recorded Japanese consumption-tax settings and journal line tax blocks,
including category, rate and simplified-taxation business class.

## Before use

Confirm taxpayer status, the taxation method and tax-inclusive or tax-exclusive
accounting before recording settings. This package does not classify untagged
lines or calculate missing amounts. It supplies the settings used by
[jp-tax-amount](../jp-tax-amount/README.md) and [jp-tax-filing](../jp-tax-filing/README.md).

See [availability and engine requirements](../../README.md#choose-a-package) and
[package installation and selection](../../README.md#use-packages-in-a-book).

## Follow the task

Task ID: `jp-tax-classification.classify`. From the Book folder:

```sh
iris context --task jp-tax-classification.classify
iris overlay guide jp-tax-classification.classification
```

Read the [workflow guide](guides/classification.md) for inputs, commands and coverage.
The [task definition](tasks.yaml) links these executable examples:

- [Settings and classification examples](tests/classification.yaml)
- [Category and rate examples](tests/tax-lines.yaml)
