# 消費税の設定と税区分を検証する

[English](README.md) | **日本語**

日本の消費税について、帳簿の設定と仕訳明細の税情報を検証します。税区分、税率、簡易課税の事業区分が対象です。

## 利用前に確認すること

課税事業者か免税事業者か、課税方式、税込・税抜の経理方式を確認してから設定します。税情報がない明細の自動分類や、未入力金額の計算は行いません。[jp-tax-amount](../jp-tax-amount/README.ja.md) と [jp-tax-filing](../jp-tax-filing/README.ja.md) も、この設定を使います。

[公開状況とエンジンの要件](../../README.ja.md#使いたいパッケージを選ぶ)、[導入と有効化の手順](../../README.ja.md#帳簿で使う)も確認してください。

## タスクに沿って進める

タスク ID は `jp-tax-classification.classify` です。帳簿フォルダーで次を実行します。

```sh
iris context --task jp-tax-classification.classify
iris overlay guide jp-tax-classification.classification.ja
```

[操作ガイド](guides/classification.ja.md)に入力、コマンド、対応範囲を記載しています。[タスク定義](tasks.yaml)から、次のテスト例も参照できます。

- [設定と税区分の例](tests/classification.yaml)
- [税区分と税率の例](tests/tax-lines.yaml)
