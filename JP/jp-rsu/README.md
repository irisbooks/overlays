# jp-rsu

Unreleased `2026.10.2` candidate, compatible with the already published signed
Iris v0.2.18 engine (bindings 5).

Validate recorded JPY RSU vesting, complete its salary credit, and summarize
posted additional gross salary for the explicitly confirmed resident-employee
self-assessment profile. There is no securities-basis package dependency.
Automatic price/FX valuation and securities/foreign-cash basis calculations remain
deferred until their core capabilities are published; this package does not
substitute generic inventory arithmetic for those policies.

[English guide](guides/vesting.md) | [日本語](README.ja.md) |
[Executable examples](tests/vesting.yaml)

This is source under review, not a signed package publication. Review valuations
and validate the Book before preparing figures. Canonical source:
`irisbooks.overlays/JP/jp-rsu`.
