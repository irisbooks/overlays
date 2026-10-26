# jp-rsu

Unreleased `2026.10.2` source candidate requiring bindings 6. Qualification uses
the published signed stable engine pinned in `.github/engine.txt`.

Calculate exact whole-share JPY vesting, complete both native posting amounts,
validate matched vesting evidence, and prepare annual additional gross salary
from complete local journals. Existing reviewed-JPY records remain supported;
complete `valuation` inputs can also supply the amount without a redundant
`gross_jpy` field. Rounding is explicit and the calculation stays in private
Overlay functions.

Salary stands alone. Select `jp-securities-basis` for share disposals and rounded
remaining basis, and `jp-foreign-currency` for ordinary USD cash realization.
Each package has its own explicit scope and account mappings. The root-Book
year-end workflow retains native carrying value and separate allocation basis.

[English guide](guides/vesting.md) | [日本語](README.ja.md) |
[Existing examples](tests/vesting.yaml) | [Valuation](tests/valuation.yaml) |
[Restored workflow](tests/full-workflow.yaml)

This is source under review, not a signed package publication. These outputs are
filing aids; named-view filings/rollover, accepted financial generations and
e-Tax submission are separate host work.
