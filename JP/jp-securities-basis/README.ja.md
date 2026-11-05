# 上場株式の取得費を計算する

[English](README.md) | **日本語**

同じ銘柄の通常購入とRSUで取得した株式を、指定した本人名義口座の全体で集計します。
売却時の帳簿価額を補完し、端数処理後の1株当たり取得価額と残存取得費を計算します。
帳簿価額と税務上の取得費は別々に保持します。

## 利用前に確認すること

指定した口座にその銘柄の対象株式がすべて含まれていること、取得費に根拠があることを
確認してください。NISA・特殊口座、端数株、未解決の約定・受渡時差には対応していません。
出力は申告準備資料で、申告書の提出は行いません。bindings 6に対応するエンジンが必要です。

[公開状況とエンジンの要件](../../README.ja.md#使いたいパッケージを選ぶ)、[導入と有効化の手順](../../README.ja.md#帳簿で使う)も確認してください。

## タスクに沿って進める

タスク ID は `jp-securities-basis.shares` です。帳簿フォルダーで次を実行します。

```sh
iris context --task jp-securities-basis.shares
iris overlay guide jp-securities-basis.shares.ja
```

[操作ガイド](guides/shares.ja.md)に入力、コマンド、対応範囲を記載しています。[タスク定義](tasks.yaml)から、次のテスト例も参照できます。

- [取得費の計算例](tests/basis.yaml)
- [取得から売却・年度繰越までの例](tests/lifecycle.yaml)
