# Propose a missing consumption-tax amount

**English** | [日本語](amount.ja.md)

First inspect `jp-tax-classification.classify` for the confirmed taxpayer status,
taxation method and accounting settings. The [classification guide](../../jp-tax-classification/guides/classification.md)
explains these fields. Both packages must be selected at the required exact versions.

On a tax-exclusive Book, classified postings are net amounts. A missing
`line.tax.amount` is proposed as net amount × rate / 100, truncating fractional
yen. Tax-inclusive Books receive no proposal, and existing amounts stay unchanged.

From the Book folder, inspect your journal and all validation hints:

```sh
iris context --task jp-tax-amount.propose --record journals/2026-10/purchase.md
iris validate
```

Replace the path with the actual journal. Review the amount basis, invoice
rounding and **all** derivation hints before running:

```sh
iris validate --apply
```

`--apply` applies eligible missing-field proposals across the Book; it is not
restricted to the journal inspected above. Local MCP `validate` reads the checks
without applying fixes. Use the CLI command explicitly when applying proposals.

The proposal records a tax amount field; it does not add a separate tax posting.
Review the complete journal and any required tax posting before posting. To stop
these proposals, omit `jp-tax-amount` from the complete selection while retaining
other desired packages; see [selection instructions](../../../README.md#use-packages-in-a-book).
The filing package is optional. See the [positive and negative examples](../tests/amount.yaml).
