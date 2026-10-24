# 少額減価償却資産の特例を検証する

[English](README.md) | **日本語**

少額減価償却資産の特例について、取得日に応じた金額基準と帳簿全体の年間限度額を検証します。適用要件を確認した資産に `method: expensed` と `toku_rei: shoutoku_300k` を指定します。

## 利用前に確認すること

納税者と資産の適用要件を確認してから `jp_deduction_confirmed` を設定します。対象は、12か月の年度で取得年に事業の用に供し、対象資産をすべて記録した帳簿です。年間限度額の確認には、帳簿全体の検証が必要です。一括償却資産には未対応です。定率法の計算は[別のパッケージ](../jp-declining-balance/README.ja.md)で行います。

[公開状況とエンジンの要件](../../README.ja.md#使いたいパッケージを選ぶ)、[導入と有効化の手順](../../README.ja.md#帳簿で使う)も確認してください。

## タスクに沿って進める

タスク ID は `jp-small-asset-deduction.equipment` です。帳簿フォルダーで次を実行します。

```sh
iris context --task jp-small-asset-deduction.equipment
iris overlay guide jp-small-asset-deduction.equipment.ja
```

[操作ガイド](guides/equipment.ja.md)に入力、コマンド、対応範囲を記載しています。[タスク定義](tasks.yaml)から、次のテスト例も参照できます。

- [金額基準と年間限度額の例](tests/equipment.yaml)
