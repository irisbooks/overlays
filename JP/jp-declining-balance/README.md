# Calculate a declining-balance schedule

**English** | [日本語](README.ja.md)

Calculates annual depreciation rows using explicit declining, guarantee and
revised rates, including the transition to the revised rate.

## Before use

Confirm method eligibility, the published rate table and full twelve-month
service years before setting `full_year_confirmed: true`. Partial first years
are unsupported. Previewing does not change an asset; saving requires an explicit
write. The calculation does not generate depreciation journals.

See [availability and engine requirements](../../README.md#choose-a-package) and
[package installation and selection](../../README.md#use-packages-in-a-book).

## Follow the task

Task ID: `jp-declining-balance.schedule`. From the Book folder:

```sh
iris context --task jp-declining-balance.schedule
iris overlay guide jp-declining-balance.schedule
```

Read the [workflow guide](guides/schedule.md) for inputs, commands and coverage.
The [task definition](tasks.yaml) links these executable examples:

- [Numerical schedule examples](tests/recipes.yaml)
- [Full-year confirmation examples](tests/coverage.yaml)
