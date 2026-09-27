# IrisBooks region overlays

**English** | [日本語](README.ja.md)

The region-specific bookkeeping and tax rules of [IrisBooks](https://irisbooks.jp),
written as YAML + [CEL](https://cel.dev). The `iris` engine knows nothing about
any one country; what differs by jurisdiction — which assets qualify for which
depreciation special, how a 消費税 line must be classified, how a return's
figures are assembled from the ledger — lives here, one directory per region.

| Path | What it holds |
|---|---|
| `<id>/overlay.yaml` | id, version, the bindings version it requires |
| `<id>/functions.yaml` | named CEL functions shared by everything below |
| `<id>/rules/` | checks — run by `iris validate`, and by the cloud on every write |
| `<id>/recipes/` | computations whose output is recorded with provenance and replayed |
| `<id>/derive/` | values `iris validate --fix` proposes for missing fields |
| `<id>/tests/` | golden cases for all of the above |

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

Overlays carry **method**, not **rates**. Anything that changes under a tax
reform without changing the method — a depreciation rate, a deemed purchase
ratio, a transitional deduction percentage — is a recipe parameter that the
user's AI looks up for the period and records on the book, never a table here.

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
