# Complete one missing journal amount

**English** | [日本語](journal.ja.md)

In an existing draft, record the date, evidence, accounts and known amounts.
Set exactly one monetary amount to `null`. From the Book folder, preview:

```sh
iris context --task journal-balance.journal --record journals/2026-10/entry.md
iris journal complete journals/2026-10/entry.md
```

Replace the example path with your draft. Inspect the complete `proposal` and
copy the returned `revision`. To apply that reviewed proposal:

```sh
iris journal complete --apply --revision REVISION_FROM_PREVIEW journals/2026-10/entry.md
iris validate
```

Local MCP uses `complete_journal(path)` for preview, then the same tool with
`apply: true` and the returned `revision` for application. Application edits the
draft; it does not post or sync. Review the transaction and evidence before any
separate posting operation. A balanced journal alone does not prove correctness.

See the [executable balancing example](../tests/autocomplete.yaml), case
`money-only balance needs no extra journal fields`. Quantity-based disposals use
[the inventory workflow](../../inventory-disposal/guides/inventory.md).
