# 日本の上場株式の取得費

通常購入とRSU取得を同じ銘柄のプールで計算する、独立した部品です。対象となる本人名義口座をすべて指定してください。国税庁No.1466の「総平均法に準ずる方法」に従い、1株当たり取得価額を円単位で切り上げ、残存取得費にもその単価を使います。元の帳簿価額と税務上の取得費は別に保持します。

`book.jp_securities_basis`に、`scope_confirmed: true`、`account_regime: ordinary-listed-shares`、`acquisition_fees_capitalized: true`、`accounts`、`commodities`、`settlement_accounts`、`fee_accounts`、`gain_account`を指定します。設定と仕訳には勘定科目の完全なパスを使います。銘柄の単位はscale 0の整数株です。購入手数料は取得額に含め、売却手数料と売却代金の円評価額は明示してください。

株式の貸方金額を未入力にして`iris journal complete`を実行すると、帳簿価額と損益を補完します。税務上の取得費は`jp-securities-basis.basis`で別に計算します。引数は`scope_confirmed: true`、`from`、`to`です。結果には売却代金、取得費、手数料、譲渡損益、残存取得費が含まれます。損益がゼロの取引では空の損益明細を置かないでください。

本人名義口座間の同一銘柄の移動は、同じ仕訳の両明細に同じ`inventory: {transfer: unique-id}`を付け、数量・帳簿価額を一致させます。売却・円転にはこの印を付けません。同日取引は日付・ファイルパス順に処理するため、実際の順序が保たれる名前を使ってください。

`iris yearend`は株数、帳簿価額、別の`allocation_cost_minor`と正確な`allocation_policy`を引き継ぎます。期首残高には取得費の根拠が必要です。時価への置換はしません。初期版は暦年・円建ての個人Book、通常の上場株式に対応します。NISA・特殊口座、端数株、空売り、デリバティブ、未解決の約定・受渡時差は対象外です。

[国税庁No.1466](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1466.htm)、[外国株式の為替換算](https://www.nta.go.jp/law/shitsugi/shotoku/02/02.htm)。候補版であり、署名済み公開版ではありません。出力は申告準備資料です。
