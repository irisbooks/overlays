# Record equipment

Confirm the asset, acquisition and service dates, supported method, useful life, amount basis, salvage and account mappings. Native expensed and straight-line calculations provide mechanical schedules; their existence does not establish a statutory method. Preview the schedule and acquisition journal before guarded application and posting. Business-use allocation is a separate core operation with explicit inputs.

## Immediate deduction

Ordinary expensing and the small-business special are distinct. The optional `toku_rei: shoutoku_300k` token uses the acquisition-date threshold, despite its historical name: under JPY 300,000 through 2026-03-31, under JPY 400,000 from 2026-04-01 through 2029-03-31. This package's special checks apply from JPY 100,000. Exactly the upper threshold is refused; dates beyond the legislated expiry are refused.

Set `jp_deduction_confirmed: true` only after checking taxpayer/asset eligibility, filing conditions, the tax accounting basis and supporting evidence. This initial package supports a twelve-month FY with service in the acquisition year and an all-book JPY 3 million cap. Short years, deferred service and incomplete asset sets are unsupported. Run whole-book validation: record context alone cannot check the annual cap. The confirmation records judgment, not proof.

## Other schedules

The declining-balance recipe requires explicit published rates, useful life and first year-end, plus `full_year_confirmed: true`. It only models full twelve-month service years. Do not use it for the usual partial acquisition year or infer rate-table eligibility from the asset label.

Three-year pooled depreciation is refused explicitly. Its annual pool deduction is not an ordinary 36-month straight-line schedule. No pool or pool-disposal contract is provided yet. Old `jp` package copies remain available for exact historical replay; they are not mixed with this package.

## Primary references

Verified 2026-10-24: [NTA individual depreciation and deductions](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2100.htm), [NTA corporate small-business special](https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5408.htm). Check eligibility and service-date conditions directly; the package does not decide them.
