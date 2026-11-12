# IrisBooks overlays

[English](README.md) | **日本語**

オーバーレイは、[IrisBooks](https://irisbooks.io/) の帳簿に検証・金額補完・計算機能を追加するパッケージです。機能ごとに入力項目、使い方のガイド、実行可能なテスト例をまとめています。必要なパッケージを帳簿ごとに有効化できます。

## 使いたいパッケージを選ぶ

以下はすべて署名付きの公開版です。

| 分類 | パッケージ | 用途 | 署名付きリリース |
|---|---|---|---|
| 仕訳補完 | [journal-balance](journal-balance/README.ja.md) | 貸借が一致するよう、未入力の金額を1件補完 | [2026.10.1](https://github.com/irisbooks/overlays/releases/tag/journal-balance%402026.10.1) |
| 仕訳補完 | [inventory-disposal](inventory-disposal/README.ja.md) | 数量・決済額・取得履歴から売却原価と損益を提案 | [2026.10.1](https://github.com/irisbooks/overlays/releases/tag/inventory-disposal%402026.10.1) |
| 日本の消費税 | [jp-tax-classification](JP/jp-tax-classification/README.ja.md) | 帳簿の税設定と仕訳明細の税区分を検証 | [2026.10.1](https://github.com/irisbooks/overlays/releases/tag/jp-tax-classification%402026.10.1) |
| 日本の消費税 | [jp-tax-amount](JP/jp-tax-amount/README.ja.md) | 税抜明細に未入力の税額を提案 | [2026.10.1](https://github.com/irisbooks/overlays/releases/tag/jp-tax-amount%402026.10.1) |
| 日本の消費税 | [jp-tax-filing](JP/jp-tax-filing/README.ja.md) | 本則課税・簡易課税の計算資料を作成 | [2026.10.1](https://github.com/irisbooks/overlays/releases/tag/jp-tax-filing%402026.10.1) |
| 日本の固定資産 | [jp-small-asset-deduction](JP/jp-small-asset-deduction/README.ja.md) | 少額資産特例の取得日別の金額基準と年間限度額を検証 | [2026.10.1](https://github.com/irisbooks/overlays/releases/tag/jp-small-asset-deduction%402026.10.1) |
| 日本の固定資産 | [jp-declining-balance](JP/jp-declining-balance/README.ja.md) | 12か月分の定率法による償却表を計算 | [2026.10.1](https://github.com/irisbooks/overlays/releases/tag/jp-declining-balance%402026.10.1) |
| 日本の株式報酬 | [jp-rsu](JP/jp-rsu/README.ja.md) | RSUの権利確定時の評価額を計算し、仕訳を補完して追加の給与収入を年単位で集計 | [2026.11.1](https://github.com/irisbooks/overlays/releases/tag/jp-rsu%402026.11.1) |
| 日本の有価証券 | [jp-securities-basis](JP/jp-securities-basis/README.ja.md) | 上場株式の端数処理後の取得費を、帳簿価額と分けて計算 | [2026.11.1](https://github.com/irisbooks/overlays/releases/tag/jp-securities-basis%402026.11.1) |
| 日本の外貨 | [jp-foreign-currency](JP/jp-foreign-currency/README.ja.md) | 通常の米ドル現預金の取得費を引き継ぎ、実現した為替差損益を計算 | [2026.11.1](https://github.com/irisbooks/overlays/releases/tag/jp-foreign-currency%402026.11.1) |

`JP/` に日本向けのパッケージをまとめ、共通パッケージはリポジトリのルートに置きます。どのパッケージを選ぶか、パッケージに含まれない作業は何かは、[日本向けの概要](JP/README.ja.md)を参照してください。フォルダーはソースを整理するためのもので、パッケージ ID、固定バージョンの指定、有効化の方法は変わりません。

`jp-tax-amount` と `jp-tax-filing` は、それぞれ `jp-tax-classification@2026.10.1` も有効にする必要があります。両者は互いには依存しません。依存先も明示的に選択してください。ほかのパッケージは個別に使えます。分類名は、パッケージを探しやすくするためのものです。

パッケージは、エンジン（`iris` コマンド本体）が提供する関数と値の仕様である「バインディング」のバージョンを指定しています。七つの `2026.10.1` はバインディングの**バージョン5**が必要で、[Iris v0.2.18](https://github.com/irisbooks/iris/releases/tag/v0.2.18) で動作を確認しています。三つの `2026.11.1` はバインディングの**バージョン6**が必要で、[Iris v0.2.23](https://github.com/irisbooks/iris/releases/tag/v0.2.23) で動作を確認しています。各リリースには、固定バージョンのパッケージ本体と署名を添付しています。ソースのテスト方法は[エンジンの要件](CONTRIBUTING.ja.md#対応するエンジンを用意する)を参照してください。

## 帳簿で使う

初めて使う方は、[CLI の導入と帳簿の作成](https://irisbooks.io/docs/ja/getting-started/)から始めてください。以下は、パッケージのバインディングと現在の CLI コマンドに対応するエンジンで、既存の帳簿フォルダーから実行する例です。

インストールすると `config/overlay-packages/` にパッケージが保存されます。その後、有効化するパッケージを選択します。次は貸借補完だけを有効にする例です。`select` は有効な一覧全体を置き換えるため、ほかに使い続けるパッケージがあれば、それも指定してください。

```sh
iris overlay install --pin journal-balance@2026.10.1
iris overlay list --json
iris overlay select --pin journal-balance@2026.10.1
iris context
iris context --task journal-balance.journal
iris overlay guide journal-balance.journal.ja
iris overlay example journal-balance.journal 'tests/autocomplete.yaml#money-only balance needs no extra journal fields'
```

依存先も含め、使うパッケージをすべて `--pin` で指定してください。変更前に `list` で現在の選択を確認し、必要なら `select --dry-run --json` で変更内容を確認できます。すべて無効にする場合は `select --off` を使います。無効にしても、記録済みの項目・結果と、過去の計算結果を再現するための定義は残ります。Iris 本体による構造と貸借の検証も続きます。

新規に作る日本向けの事業用帳簿では、既定で `2026.10.1` の七つが選択されます。個人用帳簿と日本以外の事業用帳簿では、仕訳補完の二つが選択されます。既存の帳簿は、利用者が変更するまで現在の選択を維持します。

## CLI コマンドの使い分け

| 操作 | 現在の CLI コマンド |
|---|---|
| 仕訳補完の候補を確認 | `iris journal complete <journal>` |
| 確認した補完を適用 | `iris journal complete --apply --revision HASH <journal>` |
| 仕訳と証憑の参照関係を確認 | `iris references <path>` |
| 帳簿を検証 / 確認した項目補完を適用 | `iris validate` / `iris validate --apply` |
| 計算結果を確認 / 確認した結果を保存 | `iris overlay recipe <id> --set name=value` / `--apply --out PATH` を追加 |
| 同期で拒否された操作の確認・再試行の準備 | `iris sync issues list --json` / `iris sync issues retry` |

計算と仕訳補完は、既定では結果の表示だけを行います。レシピは `--out PATH` だけでは書き込まず、保存には `--apply` も必要です。一方、パッケージの選択と更新は、既定でそのまま実行されます。`--dry-run` を付けると、変更内容の確認だけを行います。記帳（`iris post`。下書きの仕訳を記帳済みにする操作）は、これらとは別の操作です。`iris post` は、記帳したあと、連携済みの帳簿全体を同期します。このとき、ほかの未同期の変更も一緒に同期されます。`iris post --local` は、同期せずに記帳します。

上の例は帳簿フォルダーで実行します。別の場所から実行する場合は `--book-path PATH` で帳簿を指定します。サーバーの帳簿を操作するときは `--book-id ID` を使います。CLI のフラグは引数の前後どちらにも置けます。`--` 以降はフラグとして解釈しません。

パッケージのバインディングに加え、現在の CLI コマンドに対応するエンジンが必要です。パッケージを使う前に `iris journal complete --help`、`iris validate --help`、`iris overlay recipe --help` を確認してください。CLI の旧名 `autocomplete`・`show`・`attention` は削除しました。ローカル MCP は `complete_journal`・`list_sync_issues`・`retry_sync_issues` を使います。テストの `autocomplete` 項目は変わりません。

## AI アシスタントでタスクを確認する

ローカル MCP では `get_book_context`、`read_overlay_guide`、`read_overlay_example` で同じ情報を読めます。実行する前に、該当タスクの入力項目、対応範囲、テスト例を確認してください。各ガイドに CLI コマンドとローカル MCP のツール名を記載しています。詳しい構文は [CLI リファレンス](https://irisbooks.io/docs/ja/cli-reference/)を参照してください。

CLI の計算レシピは、`--apply --out PATH` を指定するまで結果の表示だけを行います。仕訳補完で編集するのは下書きであり、記帳は別の判断です。パッケージ内の説明は参照資料であり、操作の許可にはなりません。検証に通っても、税制上の適用要件を満たすことや申告書の完成を保証するものではありません。

## ローカル MCP のレシピ実行

ローカル MCP サーバーには、帳簿一つを対象にする単一帳簿モードと、複数の帳簿を収めた親フォルダーを対象にするモードがあります。どちらのモードでも `list_recipes` と `run_recipe` を使います。ID は CLI と同じ `jp-declining-balance.teiritsu` などです。レシピごとの旧 MCP ツールは削除しました。計算の入力は `params` に渡します。既定では結果を表示するだけで、`out` を指定しただけでは保存しません。確認後に保存するときは、`params` の外に `apply=true` と帳簿相対パスの `out` を指定します。旧 `write` 引数は削除しました。親フォルダーのモードでは、両ツールに `book` も必要です。不明な引数や型の誤りは実行前にエラーとなります。

## リモート MCP は読み取り専用

リモート（クラウド）MCP は、初回リリースでは帳簿を読み取るだけで、記帳はできません。帳簿に保存されているパッケージの参照情報を読めます。原資料をアップロードして保存することもできますが、その際にオーバーレイは実行されません。CEL やレシピは実行せず、仕訳も変更しません。この文書の実行・保存の例はローカル CLI とローカル MCP サーバー向けです。変更はローカルで検証してから同期します。

## 改善を提案する・問題を報告する

改善の提案方法は [CONTRIBUTING.ja.md](CONTRIBUTING.ja.md) を参照してください。問題は [GitHub の issue](https://github.com/irisbooks/overlays/issues) で報告できます。パッケージのバージョン、入力、期待する結果を添えてください。

## ライセンス

[Apache License 2.0](LICENSE)。エンジンは別の利用条件で配布します。
