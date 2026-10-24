# 消費税の設定と税区分を検証する

[English](classification.md) | **日本語**

課税事業者か免税事業者かを確認し、`config/book.yaml` の `consumption_tax.status` に `taxable` または `exempt` を記録します。設定がない場合は未確認であり、免税とは扱いません。課税事業者の帳簿では、課税方式と経理方式も確認してください。次は設定の一部です。実際に確認した値を、既存の設定に追加します。

```yaml
region: JP
currency: JPY
scale: 0
consumption_tax:
  status: taxable
  method: general        # general: 本則課税、simplified: 簡易課税
  accounting: tax_included  # tax_included: 税込、tax_excluded: 税抜
```

仕訳明細の `tax` には、税区分の `category`、税率の `rate`、必要に応じてインボイスの有無を示す真偽値の `invoice` を記録します。簡易課税の課税売上には、1〜6の `business_class` も必要です。確認済みの `consumption_tax.business_class` を帳簿の既定値として使うこともできます。

| 項目 | 指定できる値 |
|---|---|
| `category` | `taxable_sale`、`taxable_purchase`、`exempt_sale`、`exempt_purchase`、`export_sale`、`out_of_scope`、`securities_sale` |
| `rate` | `10`（標準）、`8r`（軽減）、`8o`・`5`・`3`（旧税率）。輸出売上は `0` または省略 |
| `invoice` | 記録する場合は YAML の `true` または `false` |

税込経理では仕訳の金額を税込、税抜経理では税抜で記録します。証憑、税区分、取引日に適用する税率、金額の税込・税抜の扱いは、利用者が確認してください。指定した税率の値が有効でも、その取引に適用できるとは限りません。

帳簿フォルダーで、パスを実際の仕訳に置き換えて確認します。

```sh
iris context --task jp-tax-classification.classify --record journals/2026-10/purchase.md
iris validate
```

ローカル MCP では `get_book_context` で入力を確認し、`validate` で検証します。税情報のない明細は未分類のままです。税区分や税額の補完も行いません。未入力の税額を提案する場合は [jp-tax-amount](../../jp-tax-amount/README.ja.md)、申告資料の計算には [jp-tax-filing](../../jp-tax-filing/README.ja.md) を選択します。

[設定と税区分の例](../tests/classification.yaml)、[税区分と税率のテスト](../tests/tax-lines.yaml)も参照できます。

## 根拠資料

国税庁の[令和8年度税制改正特集](https://www.nta.go.jp/taxes/shiraberu/zeimokubetsu/shohi/keigenzeiritsu/invoice-review/)を参照してください。
