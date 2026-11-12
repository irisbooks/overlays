# RSU vesting and recorded salary

**English** | [日本語](vesting.ja.md)

This package calculates the exact JPY value of whole vested shares in package
functions. It fills both missing amounts of the vesting journal together: the
share debit and the salary credit. It checks that the vesting evidence recorded
on the two lines matches, and prepares calendar-year salary figures from all
journals in the local Book.

Salary needs no securities or foreign-currency package. Select those two
separately for the later investment lifecycle. This package requires an engine
supporting bindings 6.

## Confirm the arrangement it covers

Confirm that all of the following describe the user's actual arrangement:

- ordinary employee RSUs settled in shares
- Japanese residence and service throughout the relevant period
- excluded from the domestic salary statement
- no Japanese withholding
- tax paid by self-assessment

These are facts to confirm for each user, not a rule that follows from the
employer's name. Net settlement, payroll inclusion, international service and
foreign tax credits are not covered and need a separately supported treatment.
A sell-to-cover workflow is not required.

## Configure the Book

Use a calendar-year JPY Book with scale 0 (no decimal places). Write accounts in
the settings as full account paths.

```yaml
units: [{symbol: AMZN, scale: 0}]
jp_rsu:
  scope_confirmed: true
  included_in_salary_statement: false
  japan_withholding: false
  tax_funding: self-assessment
  income_account: Income:RSU
  share_account: Assets:AMZN
  share_unit: AMZN
```

Configure the stock unit with quantity scale 0. The valuation recipe supports
whole shares only, and the package checks the declared Book unit scale. This
package does not calculate acquisition or disposal basis; a separately selected
package handles it. Dedicate the salary account to the arrangement confirmed
above. Ordinary salary and other income use separate accounts.

## Calculate the JPY vesting value

Review the recognition date, USD price and JPY/USD FX rate against original
evidence. Do not pass decimals as floating point: give each as an exact integer
coefficient and a decimal scale. USD 100.25 is coefficient `10025`, scale `2`;
JPY 150.1250/USD is coefficient `1501250`, scale `4`.

```sh
iris overlay recipe jp-rsu.vesting-value --set scope_confirmed=true \
  --set quantity=100 --set price_coefficient=10025 --set price_scale=2 \
  --set fx_coefficient=1501250 --set fx_scale=4 --set rounding=truncate
```

The exact value is JPY 1,505,003.125; this explicit truncation produces
`gross_jpy: 1505003`. `half-up` rounds a fraction of at least 0.5 upward.
There is no default rounding: confirm the applicable convention before choosing.
The package only computes the stated arithmetic. It does not certify the price
or rate you enter, and it does not choose a statutory valuation or rounding rule.

The supported range is 1..1,000,000 whole shares, a positive USD price and
JPY/USD rate each at most 1,000,000, and 0..8 decimal digits for each. The
recipe refuses zero, negative and out-of-range inputs, unsupported rounding and
a value that rounds to zero.

The functions use integers only. Quotient/remainder decomposition retains the
fractional USD amount through FX conversion and rounds only the final JPY value.
A raw product may exceed int64 even when the answer fits, so it is never formed;
within the supported range no intermediate or result overflows.

Review the returned `gross_jpy` and `valuation` map. If needed, save the
reviewed calculation with `--apply --out filings/rsu-valuation-vest-1.md`. The
saved file keeps every calculation parameter, so the calculation can be replayed
later. The recipe only returns figures and does not edit journal amounts.

Keep the statements, the dates you observed the price and rate, and the
calculation evidence under `raw/`, and reference them from the journal as
ordinary attachments. `valuation_source` only identifies the evidence. This
package neither hashes attachment contents nor authenticates them.

## Record the vest and complete the amounts

Put identical vesting evidence on the share debit line and the salary credit
line. As the basis for the amount, record either the exact `valuation` inputs
used in the calculation or the reviewed positive `gross_jpy`. A record with only
an already reviewed JPY amount remains supported: omit the optional `valuation`
map.

```yaml
lines:
  - account: Assets:AMZN
    debit: null
    quantity: 100
    unit: AMZN
    jp_rsu: &vesting
      event_id: amazon-2026-05
      grant_id: grant-1
      payer: Amazon.com Inc.
      recognition_date: '2026-05-01'
      valuation_source: raw/vesting-2026-05.pdf
      valuation:
        quantity: 100
        quantity_scale: 0
        price_coefficient: 10025
        price_scale: 2
        fx_coefficient: 1501250
        fx_scale: 4
        rounding: truncate
  - account: Income:RSU
    credit: null
    jp_rsu: *vesting
```

The journal date must match `recognition_date`. Run `iris journal complete` to
preview both amounts. Review the preview and apply it with the returned
`revision`, as for any other journal completion.

Completion and validation behave as follows:

- Completion works when both amounts are missing. It uses a general Iris
  capability, a checked posting proposal; the formula itself stays in the
  package.
- Iris checks the two-line proposal as one unit and preserves recorded amounts.
  It refuses when a recorded amount conflicts with the calculation.
- When `valuation` is recorded, every validation recomputes it with the same
  functions and checks the quantity, both amounts and any separately recorded
  `gross_jpy`. Incomplete or out-of-range calculation inputs are a validation
  error.
- It creates no cash, withholding or sale line.

Before posting and preparing figures, validate the complete Book with
`iris validate` and resolve all issues. Posting is a separate decision for the
Book's owner.

## Prepare the calendar-year additional salary

Run `jp-rsu.salary` with `scope_confirmed=true`, the configured `income_account`
and the first and last day of one calendar year.

```sh
iris overlay recipe jp-rsu.salary --set scope_confirmed=true \
  --set income_account=Income:RSU --set from=2026-01-01 --set to=2026-12-31
```

Add `--apply --out filings/rsu-salary-2026.md` to save a reviewed result; as
with other recipes, the calculation parameters are recorded with it. Local MCP
uses `complete_journal` for completion and `run_recipe` with
`recipe: jp-rsu.salary` and the same parameters for the figures. Both CLI and
MCP preview by default. Remote MCP cannot run these operations.

The recipe sums posted salary only. It requires all of the following:

- matching vesting evidence on the share line and the salary line
- unique `event_id` values
- a positive gross amount backed by evidence
- every required field on the dedicated-account lines

It refuses duplicate events, missing evidence, evidence on only one of the two
lines, inconsistent amounts, wrong accounts, reversals, and periods shorter than
or spanning beyond one calendar year.

The recipe reads all journals in the local Book and checks each posted journal's
structure, actual date and quantity before it sums the evidence. Normal Book
validation (`iris validate`) is still required. Neither this check nor a source
path authenticates attachments. Reconcile the complete list of vesting events
against broker and employer records; the recipe cannot infer a vest that is
entirely missing from the Book.

The output is additional **gross salary receipts** for the arrangement confirmed
above. It is neither separately calculated taxable salary nor tax payable.
Combine it with other salary receipts before applying the salary-income
deduction.

Saved figures record `inputs_sha256` and the versioned source contract. They
replay against the retained package and unchanged source facts; changed source
facts no longer match the saved result. Securities/FX policy snapshots and basis
continuation belong to the separately selected packages.

## Sources

Checked 2026-10-26:

- [NTA salary income](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1400.htm)
- [National Tax Tribunal RSU decision](https://www.kfs.go.jp/service/JP/88/02/index.html)

## Continue through disposal, cash realization and year-end

Select `jp-securities-basis` separately when preparing share disposal figures.
It calculates ordinary purchases and vested shares in one pool, the range over
which acquisition cost is averaged.

Select `jp-foreign-currency` when you keep the USD received from a sale as
ordinary cash. For an own-account transfer recorded as a matched pair of lines,
it carries the cost forward unchanged. It calculates later currency realization
separately from salary and securities results.

Each package needs its own confirmed scope and complete account settings.
Selecting `jp-rsu` does not enable either of them.

For year-end, use the existing `iris yearend` operation with the qualified
packages installed and selected. It carries quantity, carrying value and the
rounded allocation basis (the tax basis kept apart from carrying value) forward
as separate values. For a local successor, run
`iris yearend --local --to ../book-2027 ./book-2026`; the retained sources let
that successor run on its own. Rollover does not recognize salary again. Before
carrying state forward, confirm that the source facts are complete and that
journal paths record same-day transactions in their actual order.

Reading all journals supports at most 4096 input journals in one Book fiscal
year, subject to the engine's data and execution budgets. Unsupported or
incomplete sources and exhausted limits stop with an error. Named-view
filings/rollover and accepted financial generations are separate unfinished
host work. These packages produce filing aids rather than submitted returns.

### Follow the numeric example

A vest of 100 shares at USD 100 and JPY 150/USD creates JPY 1,500,000 of
share cost and additional gross salary. Selling 40 shares for USD 4,800 valued
at JPY 696,000 gives JPY 600,000 basis and JPY 96,000 securities gain, with
60 shares and JPY 900,000 basis remaining. Transferring that USD 4,800 between
own accounts named in the settings preserves its JPY 696,000 cash basis. A later
conversion to JPY 744,000 produces JPY 48,000 of currency gain, calculated
separately from salary and the securities gain.

The [securities guide](../../jp-securities-basis/guides/shares.md) and
[cash guide](../../jp-foreign-currency/guides/cash.md) describe their separate
settings. Their task examples cover the sale, transfer and conversion, plus
successor-state cases. Reconcile each step to actual source evidence. The
amounts above contain no fees; those guides describe the calculation when
eligible fees are recorded separately.
