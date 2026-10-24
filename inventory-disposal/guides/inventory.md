# Complete disposal cost and gain/loss

**English** | [日本語](inventory.ja.md)

Record the disposal quantity, unit, settlement and fees in a draft journal. Use
`null` for amounts to calculate. Confirm the posted acquisition history and the
annual opening cost basis, then configure `inventory.params.gain_account` in
`config/book.yaml`. FIFO is the default allocation method unless a supported
method is configured.

From the Book folder, replace the path below with your draft and preview:

```sh
iris context --task inventory-disposal.inventory --record journals/2026-10/sale.md
iris journal complete journals/2026-10/sale.md
```

Review the `allocations` and the complete `proposal`, including disposal cost,
fees and gain/loss. Apply with the `revision` returned by preview:

```sh
iris journal complete --apply --revision REVISION_FROM_PREVIEW journals/2026-10/sale.md
iris validate
```

Local MCP uses `complete_journal(path)` to preview, then `apply: true` and the
returned `revision` to apply. This edits the draft without posting or syncing.
Check the evidence and acquisition history before a separate posting operation.

Missing settlement or fee amounts, insufficient holdings and unknown opening
basis are errors. Short positions and zero-cost disposals are unsupported. Do
not substitute cost for sale proceeds. See the [FIFO and refusal examples](../tests/autocomplete.yaml)
and the [record format](https://irisbooks.io/docs/en/book-format-reference/#defaults-and-inferred-values).
