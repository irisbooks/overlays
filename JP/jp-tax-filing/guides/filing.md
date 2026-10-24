# Prepare consumption-tax calculation figures

**English** | [日本語](filing.ja.md)

These recipes produce calculation aids. Read the coverage below and reconcile
all included classified postings against evidence before setting
`scope_confirmed: true`. Omitted or false confirmation is refused. The flag
records your judgment; it cannot verify eligibility. Statutory return preparation,
submission and financial-view approval are separate work.

## Check coverage before calculation

Both recipes use posted lines at 10% or reduced/old 8% rates. Historical 5%/3%
return calculations are unsupported. `from` and `to` must be ordered and match
the confirmed tax period. Tax-inclusive amounts are gross; tax-exclusive amounts
are net. Review refunds, reversals and invoice rounding. National/local splits,
taxable-base rounding and other adjustments are outside the calculation.

The general recipe assumes full input deduction is permitted: taxable sales
ratio at least 95% and taxable sales no more than JPY 500 million. It also assumes
each non-invoice supplier is below the applicable cap; it does not group purchases
by supplier or check the cap. Confirm evidence and the cap for the tax period,
including the JPY 100 million cap for periods beginning from 2026-10-01. Partial
deduction, capital-asset adjustments, special schemes and missing classifications
are unsupported.

Non-invoice purchase deduction uses the purchase date:

| Purchase date | Deduction percentage |
|---|---|
| 2023-10-01 through 2026-09-30 | 80% |
| 2026-10-01 through 2028-09-30 | 70% |
| 2028-10-01 through 2030-09-30 | 50% |
| 2030-10-01 through 2031-09-30 | 30% |
| From 2031-10-01 | 0% |

The simplified recipe requires a valid election, business class 1–6 on every
taxable sale or a confirmed Book default, and an explicit `deemed_pct` map.
Confirm rates and any special treatment for mixed business classes. The recipe
does not choose the most advantageous method. The 20%/30% special schemes are
unsupported. If your situation is outside this coverage, do not run the recipe.

## Preview, then save a reviewed result

Inspect `iris context --task jp-tax-classification.classify` for Book tax settings,
then `iris context --task jp-tax-filing.filing` for recipe inputs. Both packages
must be selected at their required exact versions; `jp-tax-amount` is optional.

From the Book folder, this previews the general calculation for a confirmed
calendar-year 2026 tax period:

```sh
iris overlay recipe jp-tax-filing.shouhizei-general --set scope_confirmed=true --set from=2026-01-01 --set to=2026-12-31
```

For simplified taxation, use `jp-tax-filing.shouhizei-simplified` with the same
period and confirmation parameters, plus `--set deemed_pct='{"1":90,"2":80,"3":70,"4":60,"5":50,"6":40}'`
after confirming that map applies. Substitute your actual period and inputs.
Each calculation runs only when invoked.

Preview does not create a file. To save reviewed figures, repeat the command with
`--apply --out filings/consumption-tax-2026.md`, choosing the desired Book-relative
path. The file records a calculation aid and its package version, recipe and
inputs. Run `iris validate` to replay it.

Both local MCP modes use `list_recipes` to discover canonical CLI recipe IDs
and parameter schemas, then `run_recipe(recipe=ID_FROM_LIST, params={...})`
to preview. The IDs are `jp-tax-filing.shouhizei-general` and
`jp-tax-filing.shouhizei-simplified`. To record reviewed figures, add
`apply=true, out="filings/consumption-tax-2026.md"` outside `params`.
`out` alone still previews. Parent mode also requires `book` on both calls.
See [calculation examples](../tests/filings.yaml),
[confirmation cases](../tests/coverage.yaml) and [transition cases](../tests/transitions.yaml).

## Primary references

[NTA reform and transition guidance](https://www.nta.go.jp/taxes/shiraberu/zeimokubetsu/shohi/keigenzeiritsu/invoice-review/),
[NTA full input deduction](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6401.htm),
[NTA simplified business classes](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6509.htm).
