# 仕訳の未入力金額を補完する

[English](journal.md) | **日本語**

既存の下書き仕訳に、日付、証憑、勘定科目、判明している金額を記録します。補完したい金額を1件だけ `null` にし、帳簿フォルダーで次を実行します。

```sh
iris context --task journal-balance.journal --record journals/2026-10/entry.md
iris journal complete journals/2026-10/entry.md
```

パスは実際の下書きに置き換えてください。返された `proposal` の明細全体を確認し、`revision` の値を控えます。確認した候補を適用するときは、その値を指定します。

```sh
iris journal complete --apply --revision REVISION_FROM_PREVIEW journals/2026-10/entry.md
iris validate
```

ローカル MCP では `complete_journal(path)` で候補を確認し、同じツールに `apply: true` と返された `revision` を渡して適用します。適用しても仕訳は下書きのままで、転記や同期は行いません。別途転記するときは、取引と証憑を確認してください。貸借が一致するだけでは、仕訳の正しさは判断できません。

[実行可能な貸借補完の例](../tests/autocomplete.yaml)の `money-only balance needs no extra journal fields` を参照できます。数量を伴う売却は[売却原価の補完手順](../../inventory-disposal/guides/inventory.ja.md)を使います。
