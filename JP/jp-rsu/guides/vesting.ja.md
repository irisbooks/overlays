# RSUの権利確定と記帳済み給与の集計

この候補版は公開済みの署名付き Iris v0.2.18（bindings 5）で動作します。
未公開の有価証券取得費・外貨計算パッケージには依存しません。
整数株数とドル株価・円／ドル為替から円換算額を正確に計算し、仕訳の検証、
確認済み株式取得額からの給与貸方補完、確定済み給与の暦年集計を行います。
株式譲渡や外貨の取得費、源泉徴収、税額、申告書は計算しません。

通常の従業員向け株式決済RSU、日本居住・日本勤務、国内源泉徴収票への
未算入、日本の源泉徴収なし、自己申告納税という実際の運用を確認します。
会社名から推定するルールではありません。差額決済、国内給与への算入、
海外勤務、外国税額控除は別途の対応が必要です。納税のための自動売却を
必須にはしません。

帳簿を暦年・円建て・scale 0とし、完全な科目パスで設定します。

```yaml
jp_rsu:
  scope_confirmed: true
  included_in_salary_statement: false
  japan_withholding: false
  tax_funding: self-assessment
  income_account: Income:RSU
  share_account: Assets:AMZN
  share_unit: AMZN
```

株式単位の数量scaleは0に設定してください。円換算レシピは整数株数が対象です。
帳簿に設定された単位のscaleや取得費は推定しません。給与科目はこの運用専用とし、通常給与や
その他の収入を混在させないでください。

## 円建ての権利確定額を計算する

原資料から認識日、ドル株価、円／ドル為替を確認します。小数は浮動小数点で
渡さず、整数の係数と小数桁数で指定してください。例えば100.25ドルは
係数`10025`・scale `2`、1ドル150.1250円は係数`1501250`・scale `4`です。

```sh
iris overlay recipe jp-rsu.vesting-value --set scope_confirmed=true \
  --set quantity=100 --set price_coefficient=10025 --set price_scale=2 \
  --set fx_coefficient=1501250 --set fx_scale=4 --set rounding=truncate
```

正確な計算結果は1,505,003.125円で、明示した切捨てにより
`gross_jpy: 1505003`となります。`half-up`は0.5以上の端数を切り上げます。
丸め方の既定値はありません。適用する扱いを確認して選択してください。
この計算は観測値の真正性を証明せず、法定の評価日や端数処理を選びません。

関数は整数の商と余りを使い、ドル段階の端数を為替換算まで保持し、最後の
円換算額だけを丸めます。計算途中の巨大な積を直接作らないため、単純な積が
int64を超える場合も対応範囲内なら正確に計算できます。対応範囲は
1～1,000,000株、正の株価・円／ドル為替がそれぞれ1,000,000以下、各小数桁数が
0～8です。この範囲で全中間値と結果を安全に扱います。ゼロ・負値・範囲外の
入力、未対応の丸め方、丸めるとゼロになる評価額は拒否します。

出力の`gross_jpy`と`valuation`を確認してください。必要なら
`--apply --out filings/rsu-valuation-vest-1.md`で計算条件とともに保存して
再計算できます。レシピは計算結果を返し、仕訳金額を書き換えません。
確認済みの円換算額を株式借方に入力し、次の手順で給与貸方を補完します。
bindings 5の導出機能から、両方の未記入の仕訳金額を直接埋めることはできません。

原資料、観測日、計算根拠を`raw/`に保存し、通常の添付参照も記録してください。
`valuation_source`は資料の参照先であり、添付内容のハッシュ化や真正性の証明
ではありません。確認済みの円換算額だけを記録する従来の使い方も可能で、
その場合は任意の`valuation`を省略します。

株式借方と給与貸方に、同一の権利確定情報を記録します。

```yaml
lines:
  - account: Assets:AMZN
    debit: 1505003
    quantity: 100
    unit: AMZN
    jp_rsu: &vesting
      event_id: amazon-2026-05
      grant_id: grant-1
      payer: Amazon.com Inc.
      recognition_date: '2026-05-01'
      gross_jpy: 1505003
      valuation_source: raw/vesting-2026-05.pdf
      valuation:
        quantity: 100
        quantity_scale: 0
        price_coefficient: 10025
        price_scale: 2
        fx_coefficient: 1501250
        fx_scale: 4
        rounding: truncate
  - account: Income:RSU
    credit: null
    jp_rsu: *vesting
```

仕訳日と`recognition_date`を一致させ、`iris journal complete`で給与貸方を
プレビューします。通常のrevision確認付き操作で適用してください。
既存の貸借補完を使うため、株式の借方金額は入力済みである必要があります。
valuationを記録した場合は同じ関数で再計算し、給与総額・数量・仕訳金額を
検査します。計算入力の欠落や範囲外の値は明示的な検証エラーです。
両方の金額が未記入の場合や記帳額が矛盾する場合は拒否し、既存額を上書き
しません。現金・源泉徴収・売却の明細も作りません。集計前に`iris validate`で
帳簿全体を検証し、問題を解消してください。確定は別の判断です。

`jp-rsu.salary`には、`scope_confirmed=true`、設定済みの`income_account`、
同じ暦年の年初・年末を指定します。

```sh
iris overlay recipe jp-rsu.salary --set scope_confirmed=true \
  --set income_account=Income:RSU --set from=2026-01-01 --set to=2026-12-31
```

確認済みの結果は`--apply --out filings/rsu-salary-2026.md`で、通常のレシピの
出所情報とともに保存できます。ローカルMCPでは`complete_journal`と、
`recipe: jp-rsu.salary`および同じパラメータを渡す`run_recipe`を使います。
どちらも既定はプレビューです。リモートMCPでは実行しません。

集計は確定済み給与が対象です。対応する株式・給与の根拠、一意のイベント
番号、正の給与総額、専用科目の記録が必要です。重複、根拠の欠落・片側のみの
記録、金額や科目の不一致、取消仕訳、年の一部や複数年の指定は拒否します。
集計だけでは個別仕訳の日付・数量・構造や添付の真正性は確認できないため、
先に仕訳を検証してください。証券会社・勤務先の資料と全イベントを照合し、
完全性を確認します。帳簿にない権利確定は推定できません。

出力は、この運用における追加の給与**収入金額**です。RSUだけに別の給与所得
控除を適用せず、ほかの給与収入と合算して必要な計算を行ってください。
税額や提出用申告書ではありません。保存した結果は保持したパッケージと
仕訳から再計算できますが、未公開の在庫方針スナップショット、入力ハッシュ、
取得費の翌年繰越は追加していません。

2026-10-26確認の出典：

- [国税庁・給与所得](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1400.htm)
- [国税不服審判所・RSU裁決](https://www.kfs.go.jp/service/JP/88/02/index.html)
