# RSU vesting and recorded salary

This candidate runs on the signed published Iris v0.2.18 engine (bindings 5).
It has no dependency on the unreleased securities-basis or foreign-currency
packages. It validates recorded JPY gross compensation, fills a missing salary
credit from that recorded share debit, and sums posted salary for a calendar
year. It does not calculate the JPY valuation from share prices or FX rates,
securities disposal basis, foreign-cash basis, withholding, tax or a tax return.

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

Use a calendar-year JPY Book with scale 0. Define the stock unit and its quantity
scale in the ordinary Book configuration. This package does not infer the unit
scale or calculate acquisition/disposal basis. The salary account is dedicated
to this profile; ordinary salary and other income use separate accounts.

Review the recognition date and gross JPY valuation using original vesting and
valuation evidence. For example, an independently confirmed valuation of 100
shares at USD 100 and JPY 150/USD is JPY 1,500,000. Record that amount explicitly;
this package neither recomputes nor certifies those price/FX observations.
Keep the statements and calculation evidence under `raw/` with ordinary attachment
references. `valuation_source` identifies evidence; attachment contents are not
hashed or authenticated by this package.

Put identical evidence on both share and salary lines:

```yaml
lines:
  - account: Assets:AMZN
    debit: 1500000
    quantity: 100
    unit: AMZN
    jp_rsu: &vesting
      event_id: amazon-2026-05
      grant_id: grant-1
      payer: Amazon.com Inc.
      recognition_date: '2026-05-01'
      gross_jpy: 1500000
      valuation_source: raw/vesting-2026-05.pdf
  - account: Income:RSU
    credit: null
    jp_rsu: *vesting
```

The journal date must match `recognition_date`. Run `iris journal complete` to
preview the salary credit; review/apply it using the normal revision guard.
The existing balance primitive requires the share debit to be present. It
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
