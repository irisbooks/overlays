# Complete one missing journal amount

**English** | [日本語](README.ja.md)

Fills exactly one missing monetary amount so the recorded journal balances. Use
`null` for the amount to calculate in an existing draft.

## Before use

Use for journals containing monetary postings only. Check the accounts and
evidence yourself: balancing cannot establish that a transaction is correct. For
quantity-based disposals, use [inventory-disposal](../inventory-disposal/README.md).

See [availability and engine requirements](../README.md#choose-a-package) and
[package installation and selection](../README.md#use-packages-in-a-book).

## Follow the task

Task ID: `journal-balance.journal`. From the Book folder:

```sh
iris context --task journal-balance.journal
iris overlay guide journal-balance.journal
```

Read the [workflow guide](guides/journal.md) for inputs, commands and coverage.
The [task definition](tasks.yaml) links these executable examples:

- [Balancing example](tests/autocomplete.yaml)
