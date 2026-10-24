# 12か月分の定率法による償却表を計算する

[English](schedule.md) | **日本語**

定率法の適用可否、耐用年数、取得日に対応する償却率表を確認します。所定の償却率、保証率、改定償却率、初回の決算月、備忘価額を指定してください。各年の供用期間が12か月である場合に限り、`full_year_confirmed: true` を設定します。取得初年度の月割計算には対応していません。

帳簿フォルダーで `iris context --task jp-declining-balance.schedule` を確認します。次は[実行可能なテスト例](../tests/recipes.yaml)のうち、耐用年数8年の計算結果を表示するコマンドです。

```sh
iris overlay recipe jp-declining-balance.teiritsu --set full_year_confirmed=true --set cost=1000000 --set life=8 --set rate=0.250 --set guarantee=0.07909 --set revised=0.334 --set start=2027-03
```

実際には、対象資産について確認した値を指定してください。結果の表示だけでは資産ファイルを変更しません。確認した償却表を保存する場合は、同じコマンドに `--apply --out assets/2026/equipment.md` を追加し、既存の資産のパスに置き換えます。`schedule` と `schedule_source` に、償却表とパッケージのバージョン、レシピ、入力値を記録します。保存後は `iris validate` で記録済みの計算を再検証してください。

両モードとも `list_recipes` で入力形式を確認し、`run_recipe(recipe="jp-declining-balance.teiritsu", params={...})` に確認済みの同じ値を渡して結果を表示します。保存時は `params` の外に `apply=true, out="assets/2026/equipment.md"` を追加します。`out` だけでは保存しません。親モードでは両方の呼び出しに `book` も指定します。

保存しても減価償却仕訳の作成や会計ビューの承認は行いません。パッケージを有効にするだけでは、資産の税務上の償却方法は決まりません。[供用期間の確認がない場合のテスト](../tests/coverage.yaml)も参照できます。
