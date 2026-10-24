# 未入力の消費税額を提案する

[English](README.md) | **日本語**

税抜で記録した課税明細の `line.tax.amount` が未入力の場合に、税額を提案します。税抜金額に税率を掛け、1円未満を切り捨てます。

## 利用前に確認すること

[jp-tax-classification@2026.10.1](../jp-tax-classification/README.ja.md) も有効にしてください。税込の帳簿には提案せず、入力済みの税額は変更しません。請求書の端数処理を確認してから適用します。仮払・仮受消費税の仕訳明細は別途必要です。申告資料の計算パッケージは不要です。

[公開状況とエンジンの要件](../../README.ja.md#使いたいパッケージを選ぶ)、[導入と有効化の手順](../../README.ja.md#帳簿で使う)も確認してください。

## タスクに沿って進める

タスク ID は `jp-tax-amount.propose` です。帳簿フォルダーで次を実行します。

```sh
iris context --task jp-tax-amount.propose
iris overlay guide jp-tax-amount.amount.ja
```

[操作ガイド](guides/amount.ja.md)に入力、コマンド、対応範囲を記載しています。[タスク定義](tasks.yaml)から、次のテスト例も参照できます。

- [提案と入力済み金額を維持する例](tests/amount.yaml)
