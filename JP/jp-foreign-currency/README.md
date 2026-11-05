# Track ordinary USD cash realization

**English** | [日本語](README.ja.md)

Keeps the historical JPY basis of ordinary USD cash, including share-sale
proceeds, through own-account transfers, and calculates realized currency gains
separately from share gains and salary. Uses an explicitly confirmed
moving-average pool.

## Before use

Confirm the cost method and that the declared accounts hold every relevant
ordinary USD balance. Automatic MMF sweeps, margin FX, foreign tax credits and
unresolved settlement timing are excluded. The outputs are filing aids; the
package does not submit a return. It requires an engine supporting bindings 6.

See [availability and engine requirements](../../README.md#choose-a-package) and
[package installation and selection](../../README.md#use-packages-in-a-book).

## Follow the task

Task ID: `jp-foreign-currency.cash`. From the Book folder:

```sh
iris context --task jp-foreign-currency.cash
iris overlay guide jp-foreign-currency.cash
```

Read the [workflow guide](guides/cash.md) for inputs, commands and coverage.
The [task definition](tasks.yaml) links these executable examples:

- [Cash examples](tests/cash.yaml)
- [Lifecycle examples](tests/lifecycle.yaml)
