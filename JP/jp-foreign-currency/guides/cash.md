# Ordinary USD cash and currency gains

**English** | [日本語](cash.ja.md)

This package handles ordinary USD cash after an evidenced acquisition, including
share-sale proceeds. It is not RSU-specific and works on its own. It separates
the gain on a share sale from the currency gain or loss that arises while the
proceeds are held in USD.

Cost is calculated by the moving-average method. This is not a general statement
that Japanese law mandates this method for every foreign-currency asset. Before
use, confirm that the method applies and that all relevant ordinary USD holdings
are included.

## Configure the Book

Configure `book.jp_foreign_currency` as below. Include every account that holds
the owner's ordinary USD balance in `accounts`. The account names are examples.

```yaml
jp_foreign_currency:
  scope_confirmed: true
  method_confirmed: true
  method: moving-average
  account_regime: ordinary-cash
  currencies: [USD]
  accounts: ['Assets:USD']
  settlement_accounts: ['Assets:JPY']
  fee_accounts: ['Expenses:FXFees']
  gain_account: 'Income:FX'
```

## Record USD receipts

Record the JPY acquisition value and USD quantity explicitly on the receiving
line. USD quantity uses scale 2 (two decimal places): YAML `quantity: 4800`
represents USD 4,800, held internally in cents as 480000.

A share sale receiving USD 4,800 valued at JPY 696,000 gives that cash a basis
of JPY 696,000. A later conversion to JPY 744,000 realizes a JPY 48,000 currency
gain. Use the valuation of the actual date, and keep the rate kind, date and
statements as evidence. The package does not guess quote sources or fetch live
rates.

## Complete outgoing USD and prepare realized gains

Run `iris journal complete` on the draft journal of a transaction in which USD
leaves an account. For filing figures, run the `jp-foreign-currency.realized`
recipe with `scope_confirmed: true`, `from` and `to`.

`realized_fx_gain` is a preparation figure for reporting ordinary-cash currency
gains as miscellaneous income. It is separate from RSU salary and listed-stock
gains. Further tax-category adjustments are outside this package.

## Own-account transfers carry basis

A transfer of USD, kept as USD, between the owner's accounts named in the
settings uses one balanced journal. Put the same
`inventory: {transfer: unique-id}` on both the outgoing and the incoming line;
their quantity and carrying amount must match. For a transfer recorded this way,
the package carries the basis forward and creates no realization.

Currency conversion, third-party payment and purchasing another asset are
disposals, not transfers: do not mark them with `transfer`. Record fees on a
separate line. A journal using an unsupported settlement account fails.

For an evidenced transfer still in transit, use the USD clearing account named
in the settings. Do not treat a receipt without a matching outgoing line as a
transfer, and do not absorb a fee into a transfer whose quantities do not match.

## Name only confirmed fee accounts

In `fee_accounts`, name only accounts confirmed to hold expenses directly
attributable to the realizing transaction. The realized figure is net settlement
minus the allocation cost of that USD.

Separately recorded fees are deducted once. The gain credit already balances the
journal, so fees are not added to it again. This setting does not classify
arbitrary personal fees as deductible.

## Coverage and exclusions

The initial release supports ordinary USD cash in a calendar-year JPY personal
Book. Lines on the selected USD accounts must record the declared currency (USD)
and a quantity.

Sweeps into funds such as MMFs, margin trading, the tax category of interest and
dividends, and unresolved trade/settlement timing are excluded. Currencies other
than USD are not computed either. The package does not revalue at year-end or
recognize salary again.

A successor Book created with `iris yearend` carries carrying value and
allocation cost (the tax basis kept apart from carrying value) forward as
separate values.

The output is a filing aid, not a tax return.

## Sources

- NTA: [same-currency transfers](https://www.nta.go.jp/law/shitsugi/shotoku/02/39.htm), [reinvestment](https://www.nta.go.jp/law/shitsugi/shotoku/02/43.htm)
- NTA: [miscellaneous-income calculation](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1500.htm), [directly attributable expenses](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2210.htm)
- [National Tax College research on the method](https://www.nta.go.jp/about/organization/ntc/kenkyu/ronsou/114/01/index.htm) (research, not binding guidance)
