# 売却原価と損益を補完する

[English](README.md) | **日本語**

記録した数量、決済額、手数料、取得履歴から、売却原価と損益を提案します。原価の配分方法は、既定で先入先出法を使います。

## 利用前に確認すること

`config/book.yaml` の `inventory.params.gain_account` に損益科目を設定します。数量、決済額、期首の取得原価が必要です。決済額の欠落、保有数量の不足、空売り、原価ゼロの売却には対応していません。

[公開状況とエンジンの要件](../README.ja.md#使いたいパッケージを選ぶ)、[導入と有効化の手順](../README.ja.md#帳簿で使う)も確認してください。

## タスクに沿って進める

タスク ID は `inventory-disposal.inventory` です。帳簿フォルダーで次を実行します。

```sh
iris context --task inventory-disposal.inventory
iris overlay guide inventory-disposal.inventory.ja
```

[操作ガイド](guides/inventory.ja.md)に入力、コマンド、対応範囲を記載しています。[タスク定義](tasks.yaml)から、次のテスト例も参照できます。

- [先入先出法とエラーの例](tests/autocomplete.yaml)
