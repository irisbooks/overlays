# Classify consumption tax

Installation supplies tools, not taxpayer status. Set `consumption_tax.status` from confirmed facts. A taxable Book also records `method: general | simplified` and `accounting: tax_included | tax_excluded`, with JPY scale 0 and region JP. Absence does not mean exemption. Untagged lines are not automatically treated as purchases or sales.

A line's `tax` mapping records category, rate token, invoice boolean and (for simplified sales) business class 1..6, with a Book default allowed. Categories are taxable_sale, taxable_purchase, exempt_sale, exempt_purchase, export_sale, out_of_scope and securities_sale. Rate tokens 10 and 8r mean standard and reduced rates; 8o, 5 and 3 describe historical rates. Vocabulary validation does not establish eligibility or the rate for a transaction date.

Tax-included lines record gross postings. Tax-excluded lines record net postings, with separate tax postings where needed; the tax amount proposal computes net × rate / 100, truncating fractional yen. Confirm invoice rounding before applying. A proposal does not create the separate tax posting. Use the ordinary guarded preview/apply operation and validate the complete journal.

See the executable valid and invalid examples in `tests/classification.yaml` and the derivation cases in `tests/filings.yaml`.

## Primary references

Verified 2026-10-24: [NTA consumption-tax reform](https://www.nta.go.jp/taxes/shiraberu/zeimokubetsu/shohi/keigenzeiritsu/invoice-review/). Rates, eligibility and evidence remain distinct facts.
