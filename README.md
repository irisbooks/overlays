# IrisBooks overlays

**English** | [日本語](README.ja.md)

Reusable bookkeeping and tax rules for [IrisBooks](https://irisbooks.jp), written
as YAML + [CEL](https://cel.dev). `default/` supplies common journal completion;
regional packages such as `jp/` define jurisdiction-specific checks and
calculations. The `iris` engine provides the record bindings and native
calculation primitives.

| Path | What it holds |
|---|---|
| `<id>/overlay.yaml` | id, version, the bindings version it requires |
| `<id>/functions.yaml` | named CEL functions shared by everything below |
| `<id>/rules/` | checks — run by `iris validate`, and by the cloud on every write |
| `<id>/recipes/` | computations whose output is recorded with provenance and replayed |
| `<id>/completions/` | coordinated draft journal completion through native engine primitives |
| `<id>/derive/` | values `iris validate --fix` proposes for missing fields |
| `<id>/tests/` | golden cases for all of the above |

## Default package

`default/` holds universal journal completion, including balance completion and
FIFO inventory cost/gain proposals. Compatible engines bundle and include it
automatically, so simple journals need no extra policy attributes or pin. An
explicit `default@<version>` selects that version; specialist and trusted book
completions can override matching IDs. See [default/README.md](default/README.md).
The initial package requires binding version 3 and awaits the corresponding
engine release before upstream merge/tagging.

## How a book uses an overlay

Each `iris` release embeds the overlays released when it was built. A book pins
the one it validates against in `config/book.yaml`, and a tag in this repository
is exactly that pin:

```yaml
region: JP
overlay: jp@2026.09.1   # = the tag jp@2026.09.1 here
```

A pin never moves on its own; upgrading is an explicit edit. A released version
never changes either: a depreciation schedule or a return computed by a recipe
records `overlay: jp@<version>` as its source, and `iris validate` re-runs the
recipe under that version to prove the recorded figures came from their inputs.

Overlays carry the **method** and may carry the **statutory figures** it
needs — a rate, a threshold, a transitional percentage. Each figure is keyed on
the date the law keys it on (an acquisition date, a purchase date) and cites its
source, so a reform is a new version and the dates before it keep their old
figures. A figure that differs by taxpayer or by municipality, such as a
municipality's 償却資産税 rate, stays a recipe parameter that the user's AI looks
up and records on the book.

A book can add its own rules and recipes on top in `config/overlays/` — see
[the book format reference](https://irisbooks.jp/manual/en/book-format-reference/).
A book layer that proves useful beyond one book is welcome here as a pull
request; see [CONTRIBUTING.md](CONTRIBUTING.md).

## Run the tests

```sh
iris overlay test --dir jp
```

`--dir` needs `iris` v0.2.0 or later ([install](https://irisbooks.jp/start)).
The same suites run in CI on every pull request, against the latest signed
release.

## Not tax advice

Overlays check and compute what a book records. They are not tax advice and do
not replace a 税理士.

## License

[Apache License 2.0](LICENSE). Copyright 2026 The IrisBooks Authors. The `iris`
binary that loads these files is distributed separately, under its own terms.
