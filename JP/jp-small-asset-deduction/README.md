# Check the small-asset deduction

**English** | [日本語](README.ja.md)

Checks recorded small-business immediate deduction against acquisition-date cost
limits and the annual cap across the Book. The asset uses `method: expensed` and
`toku_rei: shoutoku_300k` after eligibility has been confirmed.

## Before use

Confirm taxpayer and asset eligibility before setting `jp_deduction_confirmed`.
The package supports twelve-month fiscal years with service in the acquisition
year and a complete asset set. Whole-Book validation is needed for the annual
cap. Pooled depreciation is unsupported; declining-balance calculation is a
[separate package](../jp-declining-balance/README.md).

See [availability and engine requirements](../../README.md#choose-a-package) and
[package installation and selection](../../README.md#use-packages-in-a-book).

## Follow the task

Task ID: `jp-small-asset-deduction.equipment`. From the Book folder:

```sh
iris context --task jp-small-asset-deduction.equipment
iris overlay guide jp-small-asset-deduction.equipment
```

Read the [workflow guide](guides/equipment.md) for inputs, commands and coverage.
The [task definition](tasks.yaml) links these executable examples:

- [Deduction boundaries and annual-cap examples](tests/equipment.yaml)
