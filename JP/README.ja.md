# 日本

[English](README.md) | **日本語**

このフォルダーのパッケージは、IrisBooks の帳簿に日本のルールを追加します。エンジン自体は地域に依存しません。複式簿記、仕訳、資産、レシピ、計算資料の記録はどの地域でも同じ仕組みです。日本の消費税、償却方法、少額資産の特例、株式報酬のルールは、選択したパッケージだけが提供します。法定の申告書は、パッケージが出した数値をもとに、あなたか AI が作成します。

## 日本の帳簿を作る

`iris init --region JP` で作った帳簿は、日付を日本時間で扱い、通貨の既定は JPY です。
日本向けの勘定科目表は `--chart general`・`it`・`food` から選べます。事業主貸と事業主借には
`owner: true` が付いているので、貸借対照表は青色申告決算書の並びのまま出て、純資産の
集計には含まれません。事業用の設定（`--preset` の既定）では、共通のパッケージに加えて
jp-tax-classification、jp-tax-amount、jp-tax-filing、jp-small-asset-deduction、
jp-declining-balance を選択します。当てはまらないものは `iris overlay select` で外してください。

## パッケージを選ぶ

| 状況 | 選択するパッケージ |
|---|---|
| 免税事業者（消費税の申告なし） | 消費税のパッケージは不要です。税込の金額を通常の売上・経費として記帳します。 |
| 課税事業者（課税取引の明細に税区分を付ける） | [jp-tax-classification](jp-tax-classification/README.ja.md) |
| 税抜経理（未入力の税額を提案させる） | [jp-tax-amount](jp-tax-amount/README.ja.md) を追加 |
| 消費税申告の計算資料を作る | [jp-tax-filing](jp-tax-filing/README.ja.md) を追加 |
| 定率法で償却する | [jp-declining-balance](jp-declining-balance/README.ja.md) |
| 少額減価償却資産の即時償却 | [jp-small-asset-deduction](jp-small-asset-deduction/README.ja.md) |
| RSU の権利確定、上場株式、米ドル現金 | [jp-rsu](jp-rsu/README.ja.md)、[jp-securities-basis](jp-securities-basis/README.ja.md)、[jp-foreign-currency](jp-foreign-currency/README.ja.md) |

依存するパッケージもすべて明示的に選択してください。手順は[帳簿で使う](../README.ja.md#帳簿で使う)を参照してください。各パッケージの README から使い方のガイドに進めます。

## パッケージに含まれない数値を調べる

資産、納税者、市区町村、その年の様式によって変わる数値は、パッケージに含めていません。国税庁や市区町村の最新のページで調べ、確定した値を帳簿に記録してください。記録しておけば税理士が確認できます。

- **耐用年数**：耐用年数省令の別表第一（一般の資産）と別表第二（機械及び装置）を[国税庁の耐用年数のページ](https://www.nta.go.jp/law/joho-zeikaishaku/hojin/sintaiyo/menu.htm)で調べ、資産ファイルの `useful_life_months` に記録します。使った区分は `yotaikai_class` に記録します。区分がはっきりしなければ、何の資産かを確認してください。
- **定率法の償却率**：償却率、保証率、改定償却率は別表第十で調べます。2012年4月1日以後に取得した資産は200%定率法、2007年4月1日から2012年3月31日までに取得した資産は250%定率法の表を使います。資産は取得時の表を使い続けます。調べた率を jp-declining-balance に渡します。
- **簡易課税のみなし仕入率**：jp-tax-filing に `deemed_pct` として渡します。

## 年度中の記録

- **領収書**：領収書ごとに明細を残すのは作業方針です。白色申告の記帳では、日々の合計を記載する方法も国税庁が説明しています（[No.2080](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2080.htm)）。
- **家事按分**：家事関連費は、事業分を区分できる記録が必要です（[No.2210](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2210.htm)）。`iris allocation` は、確認した割合で費用を分けます。
- **投資信託**：複数回購入した場合の取得費には法令上の計算方法があります（[No.1464](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1464.htm)）。帳簿の FIFO・移動平均は管理上の選択で、税務上の判断ではありません。基準価額は 10,000 口当たりで表示されます。NISA 口座の場合は、証券会社が示す口座区分、[金融庁の制度説明](https://www.fsa.go.jp/policy/nisa2/know/index.html)、[最新の対象商品](https://www.fsa.go.jp/policy/nisa2/products/)を確認してください。
- **即時償却する少額資産**：購入は資産の勘定科目に計上し、`iris asset depreciate` で償却します。費用にも計上すると二重になります。少額の品目に資産ファイルを作るかどうかは帳簿の持ち主が決めます。一括償却資産（`toku_rei: ikkatsu_3yr`）には未対応です。証憑を残し、処理を `notes/open-questions.md` に記録してください。
- **除却・売却**：記録した償却表の除却年度の行は、保有月数分（月割）に書き換えます。売却代金と帳簿価額の差額は、固定資産売却益、固定資産売却損、除却損に計上します。

## 申告書を作る

IrisBooks は集計し、申告書はあなたか AI が作り、提出はあなたが行います。エンジンの数値と記録した計算資料、その年の公式様式をもとに作業し、作成した様式は帳簿の `compiled/jp/<様式>/` に保存します。

- **消費税**：課税期間は、個人は暦年、法人は事業年度です。jp-tax-filing の数値には、国税と地方税の内訳、課税標準額の千円未満切り捨てを含めていません。記録した数値から計算してください。税抜経理の帳簿では、jp-tax-amount が提案した税額を仮払消費税・仮受消費税に計上します。
- **固定資産台帳と別表16**：資産ファイルと、`iris export assets --year`、`iris asset schedule --year` の出力を使います。`opening_nbv`、`period_dep`、`closing_nbv`、`accumulated`、`disposal_nbv` は CSV の値をそのまま使い、計算し直さないでください。
- **償却資産税（市区町村ごと）**：事業年度にかかわらず暦年で申告します。賦課期日は1月1日、申告期限は1月31日です。評価額は取得価額と減価残存率の表から求め、`closing_nbv` は使いません。`toku_rei: shoutoku_300k` で即時償却した資産も申告の対象です。

## 帳簿を保存する

帳簿は法定の保存期間（7年、法人の一部は最長10年）保存してください。IrisBooks は認証（JIIMA 認証など）を受けておらず、IrisBooks で付けた帳簿が優良電子帳簿の要件を満たすとは主張しません。要件を満たすかどうか、税務署への届出が必要かどうかは、あなたと税理士で判断してください。
