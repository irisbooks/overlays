# Calculate a full-year declining-balance schedule

**English** | [日本語](schedule.ja.md)

Confirm method eligibility, useful life and the rate table for the acquisition
date. Supply the published declining, guarantee and revised rates, first
year-end and salvage value. Set `full_year_confirmed: true` only when each service
year covers twelve months. Partial acquisition years are unsupported.

From the Book folder, inspect `iris context --task jp-declining-balance.schedule`.
The following previews the eight-year example in [the executable tests](../tests/recipes.yaml):

```sh
iris overlay recipe jp-declining-balance.teiritsu --set full_year_confirmed=true --set cost=1000000 --set life=8 --set rate=0.250 --set guarantee=0.07909 --set revised=0.334 --set start=2027-03
```

Use your asset's confirmed inputs. Preview prints rows without editing the asset.
To save a reviewed schedule, repeat the command with
`--apply --out assets/2026/equipment.md`, replacing the path with the existing asset.
Saving writes `schedule` and `schedule_source`, including the package version,
recipe and inputs. Run `iris validate` to replay the recorded calculation.

Both local MCP modes use `list_recipes`, then
`run_recipe(recipe="jp-declining-balance.teiritsu", params={...})` with the
same confirmed inputs to preview. To save the reviewed result, add
`apply=true, out="assets/2026/equipment.md"` outside `params`. `out` alone
still previews. Parent mode also requires `book` on both calls.

Saving creates neither depreciation journals nor financial-view acceptance.
Selecting the package does not choose the asset's tax method. See
[confirmation refusal cases](../tests/coverage.yaml).
