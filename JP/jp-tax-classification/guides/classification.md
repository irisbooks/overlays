# Check consumption-tax settings and classifications

**English** | [日本語](classification.ja.md)

Confirm taxpayer status before recording `consumption_tax.status` in
`config/book.yaml`: `taxable` or `exempt`. Missing settings leave status unknown.
For a taxable Book, confirm the taxation method and accounting basis, then merge
these fields into the existing configuration using the actual values:

```yaml
region: JP
currency: JPY
scale: 0
consumption_tax:
  status: taxable
  method: general        # general or simplified
  accounting: tax_included  # tax_included or tax_excluded
```

A journal line's `tax` mapping records `category`, `rate`, an optional `invoice`
boolean, and (for simplified taxable sales) `business_class` from 1 to 6. A
confirmed Book-level `consumption_tax.business_class` can supply the default.

| Field | Accepted values |
|---|---|
| `category` | `taxable_sale`, `taxable_purchase`, `exempt_sale`, `exempt_purchase`, `export_sale`, `out_of_scope`, `securities_sale` |
| `rate` | `10` (standard), `8r` (reduced), `8o`, `5`, `3` (historical); export sales use `0` or omit the rate |
| `invoice` | YAML `true` or `false`, when recorded |

Tax-inclusive journal amounts are gross; tax-exclusive amounts are net. Confirm
evidence, category, the rate for the transaction date and amount basis yourself.
Accepting a rate token does not establish that it applies to the transaction.

From the Book folder, replace the journal path and inspect the recorded inputs:

```sh
iris context --task jp-tax-classification.classify --record journals/2026-10/purchase.md
iris validate
```

Local MCP offers `get_book_context` for inspection and `validate` for checks.
Untagged lines stay unclassified; this package fills neither categories nor
amounts. Select [jp-tax-amount](../../jp-tax-amount/README.md) for missing tax
amount proposals or [jp-tax-filing](../../jp-tax-filing/README.md) for supporting
calculation figures.

See [settings and classification examples](../tests/classification.yaml) and
[category/rate cases](../tests/tax-lines.yaml).

## Primary references

[NTA consumption-tax reform guidance](https://www.nta.go.jp/taxes/shiraberu/zeimokubetsu/shohi/keigenzeiritsu/invoice-review/).
