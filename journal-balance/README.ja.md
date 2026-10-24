# 仕訳の未入力金額を補完する

[English](README.md) | **日本語**

既存の下書き仕訳で、貸借が一致するよう未入力の金額を1件補完します。計算したい金額に `null` を指定します。

## 利用前に確認すること

金額だけで記録する仕訳が対象です。科目と証憑は利用者が確認してください。貸借の一致だけでは取引の正しさを判断できません。数量を伴う売却には [inventory-disposal](../inventory-disposal/README.ja.md) を使います。

[公開状況とエンジンの要件](../README.ja.md#使いたいパッケージを選ぶ)、[導入と有効化の手順](../README.ja.md#帳簿で使う)も確認してください。

## タスクに沿って進める

タスク ID は `journal-balance.journal` です。帳簿フォルダーで次を実行します。

```sh
iris context --task journal-balance.journal
iris overlay guide journal-balance.journal.ja
```

[操作ガイド](guides/journal.ja.md)に入力、コマンド、対応範囲を記載しています。[タスク定義](tasks.yaml)から、次のテスト例も参照できます。

- [貸借補完の例](tests/autocomplete.yaml)
