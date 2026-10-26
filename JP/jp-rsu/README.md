# jp-rsu

Unreleased `2026.10.2` candidate, compatible with the already published signed
Iris v0.2.18 engine (bindings 5).

Calculate whole-share JPY vesting with exact Overlay functions, validate recorded
RSU postings, complete the salary credit, and summarize
posted additional gross salary for the explicitly confirmed resident-employee
self-assessment profile. There is no securities-basis package dependency.
The valuation recipe uses scaled integer price/FX inputs, explicit rounding and
bounded exact arithmetic on bindings 5. Review its output and enter the share
debit before salary-credit completion. Securities/foreign-cash basis and native
policy continuation remain separate; generic inventory arithmetic is not
substituted for those policies.

[English guide](guides/vesting.md) | [日本語](README.ja.md) |
[Executable examples](tests/vesting.yaml)

This is source under review, not a signed package publication. Review valuations
and validate the Book before preparing figures. Canonical source:
`irisbooks.overlays/JP/jp-rsu`.
