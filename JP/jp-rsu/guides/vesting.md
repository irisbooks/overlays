# RSU vesting / RSUの権利確定

Confirm the user's actual arrangement; employer identity does not determine tax handling. This profile follows the user's Amazon arrangement: vested stock is absent from the domestic salary withholding statement, there is no Japanese withholding or automatic tax sale, and tax is paid by self-assessment. Confirm Japanese residence and Japanese service throughout the relevant service period, ordinary stock settlement, and USD valuation. Other profiles need a separate reviewed treatment.

利用者が確認したAmazonでの運用として、国内給与の源泉徴収票への未算入、日本の源泉徴収なし、自己申告納税を明示します。会社名からは推定しません。権利確定時に株式の取得と給与収入を同額で記録します。ドル現金、納税、自動売却の仕訳は作りません。

Configure `book.jp_rsu: {scope_confirmed: true, included_in_salary_statement: false, japan_withholding: false, tax_funding: self-assessment, income_account: 'Income:RSU'}`. Add the exact `jp-securities-basis@2026.10.2` dependency and configure its complete share pool. On the stock debit record quantity/unit plus `jp_rsu` metadata: `event_id`, `grant_id`, `payer`, `recognition_date`, `unit_price` (decimal string), `currency: USD`, `fx_rate` (decimal string), `fx_kind: TTM`, `fx_date`, `price_source`, `fx_source`. Recognition date equals the journal date; quote date cannot be later. Use the vesting-date observation, or the applicable preceding business-day quote with the reason recorded in the evidence. Keep original statements and valuation evidence in attachments. No market data feed rewrites historical values.

Run `iris journal complete` on the vesting draft to fill the JPY stock debit and mapped salary credit. Completion changes no status beyond the existing draft workflow. For 100 shares at USD 100 and JPY 150/USD the gross salary and share cost are both JPY 1,500,000. Net-settlement, withholding or other extra lines are refused. Record actual later events in separate journals.

`jp-rsu.salary` accepts `scope_confirmed: true`, the dedicated `income_account`, and `from` / `to` dates. It reports `additional_salary_receipts`, grouped receipt evidence and zero Japanese withholding. Include that gross amount with other salary in the tax return; do not apply another salary-income deduction to RSU alone. The explicit dedicated income account detects missing vesting metadata. Duplicate event IDs fail. Confirm completeness against the vesting statement; a source missing from the Book cannot be inferred.

株式売却時までの為替変動は、円換算した株式の譲渡損益に含まれます。売却代金をドルで保有した後の円転などは、独立した外貨計算で扱います。源泉徴収票の取込みや税金のための売却は、この運用では必須にしません。

- Salary: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1400.htm
- Foreign parent share remuneration: https://www.kfs.go.jp/service/JP/88/02/index.html

Candidate source; not a signed publication. Tax-return preparation only.
