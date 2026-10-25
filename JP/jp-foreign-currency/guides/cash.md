# Ordinary USD cash / 通常のドル現金

This independent package handles ordinary USD cash after an evidenced acquisition, including share-sale proceeds. Configure `book.jp_foreign_currency` with `scope_confirmed: true`, `method_confirmed: true`, `method: moving-average`, `account_regime: ordinary-cash`, `currencies: [USD]`, `accounts`, `settlement_accounts`, `fee_accounts`, and `gain_account`. Confirm the chosen cost methodology and that all relevant ordinary USD holdings are included. It is not a general statement that Japanese law mandates this method for every foreign-currency asset.

株式の売却益と、売却代金として受け取ったドルの保有後の為替差損益を分けます。通常のドル現金に対応し、取得費の移動平均法を確認した口座だけを対象にします。外貨預金等のすべてに同じ方法が必須である、という意味ではありません。

Record the JPY acquisition value and USD quantity explicitly. Native USD quantity uses scale 2: YAML `quantity: 4800` represents USD 4,800 (480000 internally). A share sale receiving USD 4,800 valued at JPY 696,000 creates that cash basis. A later conversion to JPY 744,000 realizes JPY 48,000 FX gain. Use the actual dated valuation and preserve rate kind, date and statements in evidence; the package does not guess quote sources or fetch live rates.

Run `iris journal complete` for an outgoing USD draft and `jp-foreign-currency.realized` with `scope_confirmed: true`, `from`, `to` for filing figures. `realized_fx_gain` is an ordinary-cash miscellaneous-income preparation figure, separate from RSU salary and listed-stock gains. Further tax-category adjustments are outside this package.

A same-currency transfer between declared accounts of the same owner uses one balanced journal with the same `inventory: {transfer: unique-id}` on both legs; quantity and carrying amount must match. It carries basis and creates no realization. Currency conversion, third-party payment and purchasing another asset are disposals, not transfers. Record fees separately; unsupported settlement accounts fail.

証券口座から本人名義の銀行口座へドルのまま移すだけなら、取得費を引き継ぎ、為替差損益を作りません。円転や他の資産への支出は別取引です。MMFへの自動振替、証拠金取引、利息・配当の課税区分、未解決の受渡時差はこの初期版の対象外です。年度末の時価評価や給与の再計上は行いません。

- Same-currency transfers: https://www.nta.go.jp/law/shitsugi/shotoku/02/39.htm
- Reinvestment: https://www.nta.go.jp/law/shitsugi/shotoku/02/43.htm
- Method discussion (research, not binding guidance): https://www.nta.go.jp/about/organization/ntc/kenkyu/ronsou/114/01/index.htm

Candidate source; not a signed publication. Tax-return preparation only.
