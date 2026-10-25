# 通常のドル現金と為替差損益

RSU専用ではない、通常のドル現金の独立した計算部品です。株式売却益と、その売却代金をドルで保有した後の為替差損益を分けます。すべての外貨資産に移動平均法が必須だという意味ではありません。適用する方法と対象残高の完全性を確認してください。

`book.jp_foreign_currency`に`scope_confirmed: true`、`method_confirmed: true`、`method: moving-average`、`account_regime: ordinary-cash`、`currencies: [USD]`、`accounts`、`settlement_accounts`、`fee_accounts`、`gain_account`を設定します。対象となる本人名義の通常のドル残高をすべて含めます。

ドルを受け取ったときの円評価額とドル数量を明示します。USDのscaleは2で、YAMLの`quantity: 4800`は4,800ドル、内部値では480000です。株式売却で受け取った4,800ドルの取得費が696,000円なら、その後744,000円に円転した際の為替益は48,000円です。実際の日付の評価額・レートの種類・適用日・元の明細を残します。レートの自動推定や価格取得は行いません。

ドル支出の下書きには`iris journal complete`を使います。`jp-foreign-currency.realized`に`scope_confirmed: true`、`from`、`to`を渡すと、`realized_fx_gain`を返します。通常のドル現金の雑所得の準備額として、給与・株式譲渡益と分けます。その他の所得区分や税額調整は別途判断してください。

本人名義の証券・銀行口座へドルのまま移す場合は、同じ仕訳の両明細に同じ`inventory: {transfer: unique-id}`を付けます。数量・帳簿価額を一致させ、取得費を引き継ぎます。移動だけでは為替損益を作りません。円転、第三者への支払い、別資産の購入は処分として扱い、移動の印を付けません。手数料は別途記録します。対象外の決済科目は拒否します。

初期版は暦年・円建て個人Bookの通常のドル現金に対応します。MMFへの自動振替、証拠金取引、利息・配当の課税区分、未解決の受渡時差は対象外です。年度末の時価評価や給与の再計上はしません。

[同一通貨の移動](https://www.nta.go.jp/law/shitsugi/shotoku/02/39.htm)、[別資産への再投資](https://www.nta.go.jp/law/shitsugi/shotoku/02/43.htm)、[方法に関する税務大学校の研究（法的拘束力のある通達ではありません）](https://www.nta.go.jp/about/organization/ntc/kenkyu/ronsou/114/01/index.htm)。署名済み公開版ではない候補版です。
