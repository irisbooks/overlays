# RSU vesting and recorded salary

This candidate runs on the signed published Iris v0.2.18 engine (bindings 5).
It has no dependency on the unreleased securities-basis or foreign-currency
packages. It calculates whole-share JPY vesting with exact Overlay functions, validates
recorded compensation, fills a missing salary credit from a reviewed share debit,
and sums posted salary for a calendar year. Securities disposal basis, foreign-cash
basis, withholding, tax and tax returns remain outside this package.

Confirm the user's actual arrangement: ordinary employee stock-settled RSUs,
Japanese residence and service throughout the relevant period, exclusion from
the domestic salary statement, no Japanese withholding and tax funding by
self-assessment. These are explicit profile facts, not an Amazon-wide rule.
Net settlement, payroll inclusion, international service and foreign tax credits
need a separately supported treatment. A sell-to-cover workflow is not required.

Configure the Book using full account paths:

```yaml
jp_rsu:
  scope_confirmed: true
  included_in_salary_statement: false
  japan_withholding: false
  tax_funding: self-assessment
  income_account: Income:RSU
  share_account: Assets:AMZN
  share_unit: AMZN
```

Use a calendar-year JPY Book with scale 0 and configure the stock unit with
quantity scale 0. The valuation recipe supports whole shares only. It does not
infer the Book unit scale or calculate acquisition/disposal basis. The salary account is dedicated
to this profile; ordinary salary and other income use separate accounts.

## Calculate the JPY vesting value

Review the recognition date, USD price and JPY/USD FX observation using original
evidence. Run the valuation recipe with exact integer coefficients and decimal
scales: USD 100.25 is coefficient `10025`, scale `2`; JPY 150.1250/USD is
coefficient `1501250`, scale `4`.

```sh
iris overlay recipe jp-rsu.vesting-value --set scope_confirmed=true \
  --set quantity=100 --set price_coefficient=10025 --set price_scale=2 \
  --set fx_coefficient=1501250 --set fx_scale=4 --set rounding=truncate
```

The exact value is JPY 1,505,003.125; this explicit truncation produces
`gross_jpy: 1505003`. `half-up` rounds a fraction of at least 0.5 upward.
There is no default rounding: confirm the applicable convention before choosing.
The package computes the stated arithmetic and does not certify the observations
or choose a statutory valuation/rounding rule.

The functions use integers only. Quotient/remainder decomposition retains the
fractional USD amount through FX conversion and rounds only the final JPY value.
A raw product may exceed int64 even when the answer fits; it is never formed.
The supported range is 1..1,000,000 whole shares, positive USD price and JPY/USD
rate each at most 1,000,000, and 0..8 decimal digits for each. This bounds all
intermediates and the JPY result safely. Zero/negative/out-of-range inputs,
unsupported rounding and a value that rounds to zero refuse.

Review the returned `gross_jpy` and `valuation` map. Save the reviewed calculation
with `--apply --out filings/rsu-valuation-vest-1.md` if needed; ordinary recipe
provenance retains all calculation parameters for replay. The recipe produces
figures and does not edit journal postings. Enter its reviewed gross amount as
the share debit, then use salary-credit completion below. Published bindings 5
cannot use Overlay derivations to write both missing native posting amounts.

Keep the statements, observation dates and calculation evidence under `raw/`
with ordinary attachment references. `valuation_source` identifies evidence;
attachment contents are not hashed or authenticated by this package. An already
reviewed JPY-only valuation remains supported by omitting the optional
`valuation` map.

Put identical evidence on both share and salary lines:

```yaml
lines:
  - account: Assets:AMZN
    debit: 1505003
    quantity: 100
    unit: AMZN
    jp_rsu: &vesting
      event_id: amazon-2026-05
      grant_id: grant-1
      payer: Amazon.com Inc.
      recognition_date: '2026-05-01'
      gross_jpy: 1505003
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
preview the salary credit; review/apply it using the normal revision guard.
The existing balance primitive requires the reviewed share debit to be present.
When `valuation` is recorded, validation recomputes it with the same Overlay
functions and checks the gross amount, quantity and both postings. Incomplete or
out-of-range calculation metadata is an explicit validation error. It
refuses two missing amounts and never overwrites a conflicting recorded amount.
It creates no cash, withholding or sale line. Validate the complete Book with
`iris validate` and resolve all issues before posting and preparing figures.
Posting is a separate owner decision.

Run `jp-rsu.salary` with `scope_confirmed=true`, the configured `income_account`
and a full calendar period (`from=2026-01-01`, `to=2026-12-31`). CLI syntax:

```sh
iris overlay recipe jp-rsu.salary --set scope_confirmed=true \
  --set income_account=Income:RSU --set from=2026-01-01 --set to=2026-12-31
```

CLI `--apply --out filings/rsu-salary-2026.md` saves a reviewed result with normal
recipe provenance. Local MCP uses `complete_journal` for completion and
`run_recipe` with `recipe: jp-rsu.salary` and the same parameters. Both CLI and
MCP preview by default. Remote MCP does not execute these operations.

The recipe sums posted salary only and requires matching share/salary evidence,
unique event IDs, positive recorded gross amounts and complete dedicated-account
metadata. It refuses duplicates, missing/orphan evidence, inconsistent amounts,
wrong accounts, reversals and partial/cross-year periods. Journal validation is
still required: aggregate sums cannot prove each journal's date, quantity,
structure or attachment authenticity. Reconcile the complete event list against
broker/employer records; an entirely missing vest cannot be inferred.

The output is additional **gross salary receipts** for the declared profile,
not separately calculated taxable salary or tax payable. Combine it with other
salary receipts before the applicable salary-income deduction. Saved figures
replay against the retained package and ledger; this does not add the unpublished
inventory-policy snapshots, input hashes or basis continuation features.

Sources checked 2026-10-26:

- [NTA salary income](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1400.htm)
- [National Tax Tribunal RSU decision](https://www.kfs.go.jp/service/JP/88/02/index.html)
