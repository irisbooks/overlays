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

## Default category per account

Most accounts nearly always carry the same category: office supplies are a
taxable purchase, salaries are out of scope. List those accounts and their
usual category in `config/book.yaml`, the way accounting software sets a
default on each account:

```yaml
overlay_settings:
  jp-tax-classification:
    derivations:
      tax.category-default:
        params:
          accounts:
            '費用:消耗品費': taxable_purchase
            '費用:給料賃金': out_of_scope
            '収益:売上高': taxable_sale
```

Keys are exact account paths from the chart; values are categories from the
table above. Leave out accounts whose category depends on the transaction, such
as rent (business or residential) or miscellaneous expenses.

A line on a listed account that has no category yet gets the default as a
proposal; `iris validate` shows it and `iris validate --apply` records it. A
recorded category is never replaced. The default sets the category only: add
the rate for a taxable category, since it depends on the goods and the date.
Without these settings nothing is proposed and untagged lines stay
unclassified. This package never fills amounts. Select [jp-tax-amount](../../jp-tax-amount/README.md) for missing tax
amount proposals or [jp-tax-filing](../../jp-tax-filing/README.md) for supporting
calculation figures.

See [settings and classification examples](../tests/classification.yaml),
[category/rate cases](../tests/tax-lines.yaml) and
[default category cases](../tests/category-default.yaml).

## Primary references

[NTA consumption-tax reform guidance](https://www.nta.go.jp/taxes/shiraberu/zeimokubetsu/shohi/keigenzeiritsu/invoice-review/).
