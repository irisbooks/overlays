# 消費税の計算資料を作る

[English](README.md) | **日本語**

記帳済みの仕訳の税情報から、本則課税または簡易課税の計算資料を作ります。まず計算結果を確認します。確認した結果は、明示的に保存を指定すると、計算条件とともに `filings/` に記録できます。

## 利用前に確認すること

[jp-tax-classification@2026.10.1](../jp-tax-classification/README.ja.md) も有効にしてください。`jp-tax-amount` は不要です。ガイドの対応範囲を確認してから `scope_confirmed: true` を指定します。対象はガイドに記載した10%・8%の計算であり、出力は計算補助資料です。申告書の作成と提出は別途行います。

[公開状況とエンジンの要件](../../README.ja.md#使いたいパッケージを選ぶ)、[導入と有効化の手順](../../README.ja.md#帳簿で使う)も確認してください。

## タスクに沿って進める

タスク ID は `jp-tax-filing.filing` です。帳簿フォルダーで次を実行します。

```sh
iris context --task jp-tax-filing.filing
iris overlay guide jp-tax-filing.filing.ja
```

[操作ガイド](guides/filing.ja.md)に入力、コマンド、対応範囲を記載しています。[タスク定義](tasks.yaml)から、次のテスト例も参照できます。

- [計算例](tests/filings.yaml)
- [対応範囲の確認例](tests/coverage.yaml)
- [経過措置の期間別の例](tests/transitions.yaml)
