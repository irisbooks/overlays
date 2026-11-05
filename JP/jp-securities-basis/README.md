# Prepare Japanese listed-share basis

**English** | [日本語](README.ja.md)

Pools ordinary purchases and vested RSU shares of the same declared commodity
across the declared own accounts. Completes the recorded carrying cost of a
disposal and calculates the statutory rounded unit cost and remaining basis,
which are kept separate from the carrying value.

## Before use

Confirm that the declared accounts hold every relevant share of the commodity
and that acquisition costs are evidenced. NISA and special accounts, fractional
shares and unresolved settlement timing are unsupported. The outputs are filing
aids; the package does not submit a return. It requires an engine supporting
bindings 6.

See [availability and engine requirements](../../README.md#choose-a-package) and
[package installation and selection](../../README.md#use-packages-in-a-book).

## Follow the task

Task ID: `jp-securities-basis.shares`. From the Book folder:

```sh
iris context --task jp-securities-basis.shares
iris overlay guide jp-securities-basis.shares
```

Read the [workflow guide](guides/shares.md) for inputs, commands and coverage.
The [task definition](tasks.yaml) links these executable examples:

- [Basis examples](tests/basis.yaml)
- [Lifecycle examples](tests/lifecycle.yaml)
