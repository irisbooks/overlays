# Japanese listed-share basis / 日本の上場株式の取得費

This independent package pools ordinary purchases and vested RSU shares of the same declared commodity across the declared accounts. Confirm that the pool includes all relevant holdings. It implements the unit-cost ceiling and remaining-basis example in NTA No.1466. Native postings keep their recorded carrying value; filing figures use the separate statutory basis. No RSU metadata is required for ordinary purchases.

同じ銘柄の通常購入とRSUを、明示した本人名義口座の全体で集計します。「総平均法に準ずる方法」の1株当たり取得価額を円単位で切り上げ、売却後もその単価で残存取得費を計算します。帳簿価額と税務上の取得費を別々に保存します。購入手数料は株式取得額に含めて記録してください。

Configure `book.jp_securities_basis` with `scope_confirmed: true`, `account_regime: ordinary-listed-shares`, `acquisition_fees_capitalized: true`, `accounts`, `commodities`, `settlement_accounts`, `fee_accounts`, and `gain_account`. Use full canonical chart paths consistently in settings and journals. All commodities must be declared whole-share units (scale 0). Record the gross JPY settlement value and any sale fees explicitly. Leave the share credit amount absent for `iris journal complete`; omit an empty gain line for a zero-gain transfer. A completion fills recorded carrying cost; the `jp-securities-basis.basis` recipe computes tax figures separately.

This candidate supports a January–December JPY personal Book. It excludes NISA/special accounts, fractional shares, derivatives, short sales, and unresolved trade/settlement timing. Source journals replay by date then path; same-day source filenames must preserve actual transaction order. Mark both legs of an own-account same-commodity transfer with identical `inventory: {transfer: unique-id}` in one journal. Do not mark a sale or currency conversion as a transfer.

`iris yearend` carries quantity, recorded carrying value and the distinct `allocation_cost_minor` with exact `allocation_policy`. Opening holdings require documented basis; values are never reset to market. Save figures under `filings/` using `iris overlay recipe jp-securities-basis.basis --help` for the command syntax. This is preparation evidence, not a submitted return or an accepted financial view.

- NTA No.1466: https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1466.htm
- Foreign-stock gains: https://www.nta.go.jp/law/shitsugi/shotoku/02/02.htm

## Proceeds, fees and retained basis

Map only confirmed eligible sale fees to `fee_accounts`. The recipe derives net
settlement from the declared settlement accounts, adds the separately recorded
fees once to show gross proceeds, and subtracts allocation cost from net
settlement for the gain. It does not add fees to an income credit that already
balances a separate fee-expense line. [NTA acquisition costs and sale fees](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1464.htm).

`remaining_allocation_cost` and `remaining_carrying_value` summarize the distinct
remaining values; `basis.positions` retains per-account/unit detail. Keep all
eligible custody accounts in the declared pool. Unknown units in those accounts
and mixed acquisitions/disposals refuse; record paired own transfers separately.
Reconcile observations and fees against source statements. Missing external
events cannot be inferred from ledger totals.
