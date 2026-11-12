# Japanese listed-share basis

**English** | [日本語](shares.ja.md)

This package calculates ordinary purchases and vested RSU shares of the same
commodity in one pool, the range over which acquisition cost is averaged. It is
not RSU-specific and works on its own. Ordinary purchases need no RSU metadata.

The calculation follows the method in NTA No.1466 (総平均法に準ずる方法). The
unit cost is rounded up to whole yen, and the basis of the shares remaining
after a sale uses that unit cost too. Journal amounts keep their recorded
carrying value; filing figures use the separately calculated statutory basis.

## Configure the Book

Configure `book.jp_securities_basis` as below. Include every account that holds
the commodity for the owner in `accounts`. The account names and the commodity
are examples.

```yaml
jp_securities_basis:
  scope_confirmed: true
  account_regime: ordinary-listed-shares
  acquisition_fees_capitalized: true
  accounts: ['Assets:AMZN']
  commodities: [AMZN]
  settlement_accounts: ['Assets:JPY']
  fee_accounts: ['Expenses:ShareFees']
  gain_account: 'Income:Shares'
```

Use full account paths consistently in settings and journals. Declare every
commodity as a whole-share unit (scale 0, no decimal places). Record purchase
fees as part of the share cost, and record the gross JPY settlement value and
any sale fees explicitly.

## Complete a sale and calculate the tax basis

Leave the share credit amount absent and run `iris journal complete`; it fills
the recorded carrying cost and the gain. For an own-account transfer with no
gain, omit the empty gain line.

The `jp-securities-basis.basis` recipe computes the tax basis separately. Its
arguments are `scope_confirmed: true`, `from` and `to`. The result contains
proceeds, basis, fees, the gain and the remaining basis. Save reviewed figures
under `filings/`; see `iris overlay recipe jp-securities-basis.basis --help` for
the command syntax.

The result fields are:

- `remaining_allocation_cost`: total allocation cost (tax basis) of the shares
  remaining after the sale
- `remaining_carrying_value`: total carrying value of the same shares, a
  separate value from allocation cost
- `basis.positions`: detail per account and unit

## Proceeds and fees

In `fee_accounts`, name only accounts confirmed as eligible sale fees. The
recipe derives net settlement from the settlement accounts and adds the
separately recorded fees once to show gross proceeds. The gain is net settlement
minus allocation cost.

When fees are recorded on a separate expense line, the gain credit already
balances the journal, so fees are not added to it again.

## Own-account transfers

For a transfer of the same commodity between the owner's accounts, put the same
`inventory: {transfer: unique-id}` on both lines of one journal; their quantity
and carrying amount must match. Keep a transfer journal separate from
acquisitions and sales. Do not mark a sale or currency conversion with
`transfer`.

Journals replay by date, then by file path within a day. When several
transactions share a date, name the journal files so that path order matches
the actual transaction order.

## Carry forward to the next year

`iris yearend` carries quantity and carrying value forward. It also carries,
unchanged, the allocation cost kept apart from carrying value
(`allocation_cost_minor`) and its calculation policy (`allocation_policy`).
Opening holdings require documented basis. Values are never reset to market.

## Coverage and exclusions

The initial release supports ordinary listed shares in a calendar-year JPY
personal Book. It excludes NISA/special accounts, fractional shares, short
sales, derivatives, and unresolved trade/settlement timing.

Keep all eligible custody accounts named in the settings. Unknown units in
those accounts and mixed acquisitions and sales fail. Reconcile recorded prices,
rates and fees against source statements. Transactions missing from the Book
cannot be inferred from ledger totals.

The output is a filing aid, neither a submitted return nor an accepted
financial view.

## Sources

NTA [No.1466](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1466.htm),
[foreign-stock gains](https://www.nta.go.jp/law/shitsugi/shotoku/02/02.htm) and
[acquisition costs and sale fees](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1464.htm).
