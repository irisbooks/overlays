# RSUの権利確定と追加の給与収入を記帳する

[English](README.md) | **日本語**

整数株数の円換算を正確に計算し、株式の借方と給与の貸方を同時に補完します。
対応する権利確定の根拠を検証し、完全なローカル台帳から追加給与収入を暦年で集計します。
確認済みの円換算額は引き続き使えます。完全な`valuation`入力がある場合は、
同じ金額を`gross_jpy`に重ねて記録する必要はありません。端数処理を明示し、
計算はOverlay内の非公開関数で行います。

## 利用前に確認すること

給与の記録だけなら他のパッケージは不要です。株式譲渡と端数処理後の取得費には
`jp-securities-basis`、通常の米ドル現預金の実現差損益には`jp-foreign-currency`を
独立して選択します。各パッケージで対応範囲と科目を明示します。
`iris yearend`は、帳簿価額と別の配分取得費を翌年度へ引き継ぎます。

出力は申告準備資料です。申告書の提出や財務ビューの承認は行いません。
bindings 6に対応するエンジンが必要です。

[公開状況とエンジンの要件](../../README.ja.md#使いたいパッケージを選ぶ)、[導入と有効化の手順](../../README.ja.md#帳簿で使う)も確認してください。

## タスクに沿って進める

タスク ID は `jp-rsu.vesting` です。帳簿フォルダーで次を実行します。

```sh
iris context --task jp-rsu.vesting
iris overlay guide jp-rsu.vesting.ja
```

[操作ガイド](guides/vesting.ja.md)に入力、コマンド、対応範囲を記載しています。[タスク定義](tasks.yaml)から、次のテスト例も参照できます。

- [評価計算例](tests/valuation.yaml)
- [権利確定の記帳例](tests/vesting.yaml)
- [一連のワークフロー](tests/full-workflow.yaml)
