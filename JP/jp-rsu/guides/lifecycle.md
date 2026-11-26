# RSU vest, sale and wire: which package gives which figure

**English** | [日本語](lifecycle.ja.md)

Record a vest with its yen value on both postings and its evidence on the salary
line. Three packages then each prepare one figure for your return, or for the
accountant who prepares it:

| Figure | Package and recipe | What it is |
|---|---|---|
| `additional_salary_receipts`, `by_payer`, `records` | `jp-rsu.salary` | Gross salary from RSUs not on your salary statement, in total and by payer. Add it to your other salary before the employment income deduction. |
| `taxable_gain`, `acquisition_cost`, `remaining_allocation_cost` | `jp-securities-basis.basis` | The gain on shares you sold. Vested and bought shares of the same stock share one averaged cost. |
| `realized_fx_gain` | `jp-foreign-currency.realized` | The currency gain on ordinary USD cash, such as sale proceeds you later convert or wire. It is separate from salary and the share gain. |

None of these packages calculates tax or prepares the return itself.

## Select the packages

Salary needs only `jp-rsu`. Select `jp-securities-basis` when you sell shares and
`jp-foreign-currency` when you hold, convert or wire USD. Each package has its own
settings block: see the [vesting guide](vesting.md#configure-the-book),
`iris overlay guide jp-securities-basis.shares` and
`iris overlay guide jp-foreign-currency.cash`. Selecting `jp-rsu`
never selects the other two.

## Record the vest

Record the yen value on both postings. Put the evidence on the salary line only:
`event_id` identifies the vest, `payer` is who granted it, and `valuation_source`
points at the statement in `raw/`. Names below are examples.

```yaml
date: 2026-05-15
status: posted
lines:
  - account: Assets:EXMP
    debit: 250005
    quantity: 10
    unit: EXMP
  - account: Income:RSU
    credit: 250005
    jp_rsu: {event_id: vest-2026-05, payer: Example Corp., valuation_source: raw/vest-2026-05.pdf}
```

The share debit is the shares' starting cost, and it must equal the salary
credit: shares received as pay cost what was taxed as pay. Not zero, and not
increased by the tax you pay later. The `rsu.valuation` rule refuses a vest
whose amounts differ. You can leave the salary credit blank; `iris journal
complete` fills it from the share debit.

The package does not decide which price and exchange rate value the vest.
Confirm that for your plan and keep the statements. To have iris calculate the
yen value from the price and rate instead, use the two-line form in the
[vesting guide](vesting.md#calculate-the-jpy-vesting-value).

## Record the sale and the wire

Record a sale with its yen proceeds and leave the share credit blank; `iris
journal complete` fills the carrying cost and the gain. A wire can hold a
transfer, a conversion and a fee: record a fee on its own line, and a transfer of
USD kept as USD as `iris overlay guide jp-foreign-currency.cash` describes.
No package fetches prices or rates; record the yen for each date from your
statements.

## Prepare the figures

```sh
iris overlay recipe jp-rsu.salary --set scope_confirmed=true \
  --set income_account=Income:RSU --set from=2026-01-01 --set to=2026-12-31
iris overlay recipe jp-securities-basis.basis --set scope_confirmed=true \
  --set from=2026-01-01 --set to=2026-12-31
iris overlay recipe jp-foreign-currency.realized --set scope_confirmed=true \
  --set from=2026-01-01 --set to=2026-12-31
```

Each shows its figures. Add `--apply --out filings/<name>.md` to save one with
the inputs it came from.

## Worked example

For this year the three packages return the figures below:

| Date | Event | Yen |
|---|---|---|
| 1 Mar | Buy $1,000 | 140,000 |
| 15 May | 10 shares vest | 250,005 |
| 15 Aug | 7 shares vest | 190,003 |
| 16 Aug | Sell 12 shares for $2,200 | 330,000 |
| 18 Aug | Wire the $2,200: $25 fee, $2,175 converted at 151 | 328,425 received |

| Figure | Result | How |
|---|---|---|
| Salary | 440,008, all Example Corp. | The two vests |
| Share gain | 19,404 | 17 shares cost 440,008, so 25,882.8 each, rounded up to 25,883; 12 shares cost 310,596 |
| Currency gain | 5,300 | $3,200 cost 470,000, so the $2,200 cost 323,125; 328,425 received less that cost |

Taking the broker's per-lot cost for the share basis, or the sale's own value
for the USD, gives a different and wrong figure. The averages above are why the
share and USD packages exist.

## What stays with you

- Check that every vest, sale and wire is recorded, against your broker's and
  employer's records. The packages cannot see what the Book does not hold.
- Confirm the valuation convention and the rates for each date.
- The employment income deduction, tax, any foreign tax credit and the return.
- Not covered: shares sold or withheld at vest to pay tax (sell-to-cover, net
  settlement), fractional shares, NISA or special accounts, and a sale whose
  trade and settlement dates are not resolved.
