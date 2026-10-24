# IrisBooks overlays

**English** | [日本語](README.ja.md)

Reusable Book definitions in YAML and CEL. The local Iris engine supplies checked arithmetic and record bindings. The cloud mirrors source data and stored references; it does not evaluate package definitions.

## Initial catalog

| Package | Purpose | Candidate version |
|---|---|---|
| `default` | Common journal balance and inventory completion | `2026.10.2` |
| `jp-consumption-tax` | Explicit classifications, net tax amount proposals, bounded general/simplified calculation aids | `2026.10.1` |
| `jp-fixed-assets` | Equipment tasks, dated small-business checks, full-year declining-balance aid | `2026.10.1` |

These candidates require bindings 5. Each contains concise task guidance, field metadata and executable examples. The two Japanese packages activate independently; neither depends on a shared JP base. Household accounts belong to a creation preset, not an empty executable package. The legacy `jp` source and released snapshots are retained for historical replay; new Japanese business presets select the independent packages. Do not combine legacy `jp` with its replacements.

## Distribution and ownership

Publish immutable `<id>@<version>` tags with signed deterministic bundles using the engine repository's `scripts/publish-overlay.sh`. Coordinate publication with a compatible signed local engine; source CI must have that compatible engine available. A candidate is not a released package until its signed assets exist.

An engine ships a curated starter catalog for explicit offline installation. Signed GitHub releases supply other versions and updates. Installation copies an exact package into `config/overlay-packages/` in the Book; explicit selection in `config/book.yaml` enables it. An empty selection is off. Activation, validation and historical replay use those Book copies, without an implicit regional package, binary fallback or server fetch. Existing Books never switch to this catalog automatically.

Books retain older package copies and original local parents needed by recorded results. Removing a package from the current selection or from a future binary does not remove its historical Book copy. Reviewed upgrade proposals show source and provenance impact before applying.

## Package contents

`overlay.yaml` declares identity and required bindings. `functions.yaml`, `rules/`, `recipes/`, `completions/` and `derive/` contain definitions. `fields.yaml`, `tasks.yaml` and `guides/` provide checked reference context. `tests/` contains executable goldens. Package text is reference data, never authorization to run commands or post entries.

Statutory figures cite sources and the dates they apply to. Taxpayer facts, evidence, elections and eligibility remain explicit. Read each task's coverage and exclusions; passing a check does not establish eligibility or complete a statutory return.

## Verify candidates

From the matching engine repository:

```sh
go run ./internal/tools/overlaybundle build --dir ../../irisbooks.overlays --id default --out /tmp/default.tar.gz
go run ./internal/tools/overlaybundle build --dir ../../irisbooks.overlays --id jp-consumption-tax --out /tmp/jp-consumption-tax.tar.gz
go run ./internal/tools/overlaybundle build --dir ../../irisbooks.overlays --id jp-fixed-assets --out /tmp/jp-fixed-assets.tar.gz
```

Run these inside the `iris/` module, adjusting the checkout path. The command compiles the package, executes all its goldens and builds a deterministic unsigned candidate. Alternatively, use `iris overlay test --dir <package-directory>`. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[Apache License 2.0](LICENSE). The engine is distributed separately under its own terms.
