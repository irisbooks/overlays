# Record RSU vesting and additional salary

**English** | [日本語](README.ja.md)

Calculates exact whole-share JPY vesting, completes both native posting amounts,
validates matched vesting evidence, and prepares annual additional gross salary
from complete local journals. Existing reviewed-JPY records remain supported;
complete `valuation` inputs can also supply the amount without a redundant
`gross_jpy` field. Rounding is explicit and the calculation stays in private
Overlay functions.

## Before use

The package covers ordinary employee RSUs settled in shares, for a Japanese
resident working in Japan with no Japanese withholding. See the
[workflow guide](guides/vesting.md) for the full conditions.

Salary stands alone. Select `jp-securities-basis` for share disposals and rounded
remaining basis, and `jp-foreign-currency` for ordinary USD cash realization.
Each package has its own explicit scope and account mappings. `iris yearend`
carries the native carrying value and the separate allocation basis forward.

The outputs are filing aids. The package does not submit a return or accept a
financial view. It requires an engine supporting bindings 6.

See [availability and engine requirements](../../README.md#choose-a-package) and
[package installation and selection](../../README.md#use-packages-in-a-book).

## Follow the task

Task ID: `jp-rsu.vesting`. From the Book folder:

```sh
iris context --task jp-rsu.vesting
iris overlay guide jp-rsu.vesting
```

Read the [workflow guide](guides/vesting.md) for inputs, commands and coverage.
The [task definition](tasks.yaml) links these executable examples:

- [Valuation examples](tests/valuation.yaml)
- [Vesting examples](tests/vesting.yaml)
- [Full workflow](tests/full-workflow.yaml)

## Follow a vest through sale and wire

Task ID: `jp-rsu.lifecycle`. Record the yen on both postings with the evidence on
the salary line, and prepare salary by payer here, the share gain with
`jp-securities-basis` and the currency gain with `jp-foreign-currency`:

```sh
iris context --task jp-rsu.lifecycle
iris overlay guide jp-rsu.lifecycle
```

The [lifecycle guide](guides/lifecycle.md) maps each figure to its package and
works through a year. [Recorded-form examples](tests/recorded.yaml) cover the
vest itself.
