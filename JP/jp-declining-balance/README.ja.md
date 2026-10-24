# 定率法の償却表を計算する

[English](README.md) | **日本語**

償却率、保証率、改定償却率を指定し、年度ごとの償却額を計算します。改定償却率への切り替えも含みます。

## 利用前に確認すること

定率法の適用可否、所定の償却率表、各年の供用期間が12か月であることを確認してから `full_year_confirmed: true` を指定します。初年度の月割計算には未対応です。結果の表示だけでは資産を変更せず、保存先の指定が必要です。減価償却の仕訳は作成しません。

[公開状況とエンジンの要件](../../README.ja.md#使いたいパッケージを選ぶ)、[導入と有効化の手順](../../README.ja.md#帳簿で使う)も確認してください。

## タスクに沿って進める

タスク ID は `jp-declining-balance.schedule` です。帳簿フォルダーで次を実行します。

```sh
iris context --task jp-declining-balance.schedule
iris overlay guide jp-declining-balance.schedule.ja
```

[操作ガイド](guides/schedule.ja.md)に入力、コマンド、対応範囲を記載しています。[タスク定義](tasks.yaml)から、次のテスト例も参照できます。

- [償却表の計算例](tests/recipes.yaml)
- [12か月の供用期間の確認例](tests/coverage.yaml)
