# Complete disposal cost and gain/loss

**English** | [日本語](README.ja.md)

Proposes disposal cost and gain/loss from recorded quantities, settlement, fees
and acquisition history. FIFO is the default cost allocation method.

## Before use

Configure `inventory.params.gain_account` in `config/book.yaml`. Quantities,
settlement and opening cost basis must be known. Missing settlement, insufficient
holdings, short positions and zero-cost disposals are unsupported.

See [availability and engine requirements](../README.md#choose-a-package) and
[package installation and selection](../README.md#use-packages-in-a-book).

## Follow the task

Task ID: `inventory-disposal.inventory`. From the Book folder:

```sh
iris context --task inventory-disposal.inventory
iris overlay guide inventory-disposal.inventory
```

Read the [workflow guide](guides/inventory.md) for inputs, commands and coverage.
The [task definition](tasks.yaml) links these executable examples:

- [FIFO and refusal examples](tests/autocomplete.yaml)
