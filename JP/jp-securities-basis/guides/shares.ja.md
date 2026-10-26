# 日本の上場株式の取得費

通常購入とRSU取得を同じ銘柄のプールで計算する、独立した部品です。対象となる本人名義口座をすべて指定してください。国税庁No.1466の「総平均法に準ずる方法」に従い、1株当たり取得価額を円単位で切り上げ、残存取得費にもその単価を使います。元の帳簿価額と税務上の取得費は別に保持します。

`book.jp_securities_basis`に、`scope_confirmed: true`、`account_regime: ordinary-listed-shares`、`acquisition_fees_capitalized: true`、`accounts`、`commodities`、`settlement_accounts`、`fee_accounts`、`gain_account`を指定します。設定と仕訳には勘定科目の完全なパスを使います。銘柄の単位はscale 0の整数株です。購入手数料は取得額に含め、売却手数料と売却代金の円評価額は明示してください。

株式の貸方金額を未入力にして`iris journal complete`を実行すると、帳簿価額と損益を補完します。税務上の取得費は`jp-securities-basis.basis`で別に計算します。引数は`scope_confirmed: true`、`from`、`to`です。結果には売却代金、取得費、手数料、譲渡損益、残存取得費が含まれます。損益がゼロの取引では空の損益明細を置かないでください。

本人名義口座間の同一銘柄の移動は、同じ仕訳の両明細に同じ`inventory: {transfer: unique-id}`を付け、数量・帳簿価額を一致させます。売却・円転にはこの印を付けません。同日取引は日付・ファイルパス順に処理するため、実際の順序が保たれる名前を使ってください。

`iris yearend`は株数、帳簿価額、別の`allocation_cost_minor`と正確な`allocation_policy`を引き継ぎます。期首残高には取得費の根拠が必要です。時価への置換はしません。初期版は暦年・円建ての個人Book、通常の上場株式に対応します。NISA・特殊口座、端数株、空売り、デリバティブ、未解決の約定・受渡時差は対象外です。

[国税庁No.1466](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1466.htm)、[外国株式の為替換算](https://www.nta.go.jp/law/shitsugi/shotoku/02/02.htm)。候補版であり、署名済み公開版ではありません。出力は申告準備資料です。

## 売却代金・手数料・残存取得費

`fee_accounts`には、売却費用として扱うことを確認した科目だけを指定します。
決済科目から受取純額を求め、別途記録した手数料を一度だけ加えて売却総額を示します。
譲渡損益は受取純額から配分取得費を差し引いた金額です。
手数料を費用明細に記帳している場合、貸借を合わせる損益科目の金額に手数料を再加算しません。
[国税庁：株式等の取得費・売却手数料](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1464.htm)。

`remaining_allocation_cost`と`remaining_carrying_value`は残存配分取得費と帳簿価額の合計、
`basis.positions`は科目・単位ごとの内訳です。対象となる保管口座をすべて指定してください。
指定口座の未対応単位や取得と譲渡の混在は拒否します。本人名義の口座移動は対応する組で別仕訳にします。
観測値と手数料を原資料に照合してください。記帳されていない外部取引は合計から推定できません。
