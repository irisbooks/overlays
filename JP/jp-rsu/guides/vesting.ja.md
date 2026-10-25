# RSUの権利確定と給与収入

利用者が確認したAmazonでの運用として、国内給与の源泉徴収票への未算入、日本の源泉徴収なし、自己申告納税を明示します。会社名からは推定しません。関連する勤務期間を通じて日本居住・日本勤務であり、通常の株式交付型RSU・ドル建て評価であることを確認してください。

`book.jp_rsu`に`scope_confirmed: true`、`included_in_salary_statement: false`、`japan_withholding: false`、`tax_funding: self-assessment`、`income_account: Income:RSU`を指定します。`jp-securities-basis@2026.10.2`を同時に選択し、その株式プールも設定します。

株式取得の借方に株数・単位を記入し、`jp_rsu`に`event_id`、`grant_id`、`payer`、`recognition_date`、`unit_price`、`currency: USD`、`fx_rate`、`fx_kind: TTM`、`fx_date`、`price_source`、`fx_source`を記録します。株価・レートは文字列の小数です。認識日は仕訳日と一致させ、為替観測日はそれ以後にしません。権利確定日、または適用する直前営業日の観測値とその理由を根拠に残します。元の明細・株価・為替資料を添付し、後日の価格更新で上書きしません。

`iris journal complete`で円建ての株式取得額と同額の給与を補完します。100株・1株100ドル・1ドル150円なら、株式と給与はいずれも150万円です。ドル現金、税金のための売却、源泉徴収は作りません。税控除・純額交付・その他の明細はこの初期版では拒否します。実際の別取引は別仕訳にしてください。

`jp-rsu.salary`は`scope_confirmed: true`、専用の`income_account`、`from`、`to`を受け取り、`additional_salary_receipts`として追加する給与収入を返します。源泉徴収票の取込みも株式売却も必須ではありません。他の給与と合わせて申告し、RSUだけに給与所得控除をもう一度適用しません。権利確定資料との照合で完全性を確認してください。イベント番号の重複と、専用給与科目の根拠不足は拒否します。

株式売却までの為替変動は株式の譲渡損益に含めます。売却代金のドルを保有した後の円転等は、独立した外貨計算で扱います。年度繰越で給与を再計上しません。非居住・海外勤務、現金決済型、その他の源泉徴収・口座制度には別の判断が必要です。

[国税庁の給与所得](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1400.htm)、[外国親会社からの株式報酬](https://www.kfs.go.jp/service/JP/88/02/index.html)。署名済み公開版ではない候補版です。出力は申告準備資料です。
