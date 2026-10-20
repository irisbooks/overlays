# Default overlay

Universal journal autocomplete, included automatically by compatible IrisBooks
engines. It requires binding version 3; the engine release that provides that
binding must ship before this package is merged/tagged for release.

- `journal.balance` completes one missing balancing money amount.
- `inventory.complete` fills disposal cost and proposes a gain/loss posting.
  FIFO is implicit; `inventory.params.method` can override it. Configure
  `inventory.params.gain_account` once in the book. Quantities, proceeds and
  fees stay explicit. Acquisition history and annual opening basis fund sales.

No additional journal policy fields or default pin are required. The engine's
bundled version supplies the implicit default. A book may explicitly pin a
`default@<version>` package to select a different available version; do not mix
its definitions with a newer implicit package. Selected specialist or trusted
book-local completions override matching default IDs. Different active proposals
must agree. Native checked arithmetic stays in the engine.

Run `iris overlay test --dir default` with a binding-v3 engine. Autocomplete
golden cases supply `autocomplete.chart`, `autocomplete.journal` and optional
`autocomplete.history`; `lines` pins the complete result in journal syntax.
An `error` substring instead requires rejection. Synthetic source paths are
stable, and history is ordered by each journal's date.
