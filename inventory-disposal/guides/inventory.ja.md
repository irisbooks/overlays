# 売却原価と損益を補完する

[English](inventory.md) | **日本語**

下書き仕訳に、売却数量、単位、決済額、手数料を記録します。計算したい金額は `null` にします。転記済みの取得履歴と期首の取得原価を確認し、`config/book.yaml` の `inventory.params.gain_account` に損益科目を設定してください。対応する別の方法を設定しなければ、先入先出法で原価を配分します。

帳簿フォルダーで、次のパスを実際の下書きに置き換えて候補を確認します。

```sh
iris context --task inventory-disposal.inventory --record journals/2026-10/sale.md
iris journal complete journals/2026-10/sale.md
```

`allocations` の原価配分と `proposal` の仕訳全体を確認します。売却原価、手数料、損益を確認したら、返された `revision` の値を指定して適用します。

```sh
iris journal complete --apply --revision REVISION_FROM_PREVIEW journals/2026-10/sale.md
iris validate
```

ローカル MCP では `complete_journal(path)` で候補を確認し、`apply: true` と返された `revision` を渡して適用します。適用するのは下書きへの変更だけで、転記や同期は行いません。別途転記するときは、証憑と取得履歴を確認してください。

決済額・手数料の欠落、保有数量の不足、期首の取得原価が不明な場合はエラーになります。空売りと原価ゼロの売却には未対応です。売却代金の代わりに取得原価を使わないでください。[先入先出法とエラーのテスト例](../tests/autocomplete.yaml)、[記録形式](https://irisbooks.io/docs/ja/book-format-reference/#defaults-and-inferred-values)も参照できます。
