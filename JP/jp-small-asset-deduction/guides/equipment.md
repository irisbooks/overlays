# Check small-asset immediate deduction

**English** | [日本語](equipment.ja.md)

Confirm the asset, acquisition and service dates, method, useful life, amount
basis, salvage and account mappings. Inspect an existing asset from the Book
folder, replacing the example path:

```sh
iris context --task jp-small-asset-deduction.equipment --record assets/2026/laptop.md
iris asset schedule
iris validate
```

Local MCP provides `get_book_context` for task and record inspection,
`asset_schedule` for schedules and `validate` for whole-Book checks. Record-level
context alone cannot check the annual deduction cap. Check the linked acquisition
journal and evidence before any separate posting operation. Core expensed and
straight-line schedules perform arithmetic; tax-method eligibility and
business-use allocation need separate confirmation.

## Immediate deduction coverage

Ordinary expensing and the small-business special are distinct. For the special,
use `method: expensed` and `toku_rei: shoutoku_300k`. Despite its historical name,
the token uses the acquisition-date cost limit:

| Acquisition date | Acquisition cost supported by the special checks |
|---|---|
| Through 2026-03-31 | At least JPY 100,000 and under JPY 300,000 |
| 2026-04-01 through 2029-03-31 | At least JPY 100,000 and under JPY 400,000 |
| After 2029-03-31 | Unsupported after the legislated expiry |

Exactly the upper limit is refused. Set `jp_deduction_confirmed: true` only after
checking taxpayer and asset eligibility, filing conditions, accounting basis and
evidence. The package supports a twelve-month fiscal year, service in the
acquisition year and a JPY 3 million annual cap across all relevant assets in the
Book. Short years, deferred service and incomplete asset sets are unsupported.
The flag records your judgment; it cannot verify these facts.

## Other schedules

Use [jp-declining-balance](../../jp-declining-balance/README.md) for its separate
full-year declining-balance calculation. Three-year pooled depreciation is
unsupported. Its annual deduction cannot be represented by an ordinary 36-month
straight-line schedule; pool disposal is also outside coverage.

See [cost boundaries and annual-cap examples](../tests/equipment.yaml).

## Primary references

Check eligibility and service-date conditions directly in the
[NTA individual depreciation and deductions guidance](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2100.htm)
and [NTA corporate small-business special guidance](https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5408.htm).
