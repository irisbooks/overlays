# Prepare calculation figures

These recipes produce reproducible arithmetic aids, not a completed statutory return or an approved financial view. Read the exact Book package, confirm all assumptions, then pass `scope_confirmed: true`, `from`, `to` and the recipe-specific inputs. False or omitted confirmation is refused. Reconcile every included classified posting and preserve supporting evidence.

## Coverage

Both recipes cover posted lines with standard 10% or reduced/old 8% tokens. Historical 5%/3% return calculations are unsupported. The period must be ordered and correspond to the confirmed tax period. On tax-included Books postings are gross; on tax-excluded Books they are net. Refunds, reversals and invoice rounding need review. National/local splits, taxable-base rounding, adjustments and the statutory form are separate work.

General arithmetic assumes full input deduction is permitted (taxable sales ratio at least 95% and taxable sales no more than JPY 500 million) and that each non-invoice supplier remains below the applicable cap. Supplier identity and cap are not calculated here. The non-invoice purchase deduction is 80% through 2026-09-30, 70% through 2028-09-30, 50% through 2030-09-30, 30% through 2031-09-30, then zero; the rate follows purchase date. Confirm required evidence and the supplier cap for the tax period, including the JPY 100 million cap for periods beginning from 2026-10-01. Partial deduction, capital-asset adjustments, special schemes and missing classifications are outside coverage.

Simplified arithmetic requires a valid election, class 1..6 on every taxable sale or a confirmed Book default, and an explicit `deemed_pct` map. Confirm the applicable deemed rates and any special mixed-business treatment; no election or advantageous-method choice is inferred. The 20%/30% special schemes are unsupported.

If these conditions are not met, do not invoke the recipe. The confirmation records human judgment and does not verify it. Use the examples for arithmetic boundaries, not as evidence of taxpayer eligibility.

## Primary references

Verified 2026-10-24: [NTA 2026 reform and transition](https://www.nta.go.jp/taxes/shiraberu/zeimokubetsu/shohi/keigenzeiritsu/invoice-review/), [NTA full input deduction](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6401.htm), [NTA simplified calculation](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6509.htm).
