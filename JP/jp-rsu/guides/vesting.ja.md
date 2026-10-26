# RSUの権利確定と記帳済み給与の集計

この候補版は公開済みの署名付き Iris v0.2.18（bindings 5）で動作します。
未公開の有価証券取得費・外貨計算パッケージには依存しません。
円建ての給与総額を検証し、記帳済みの株式取得額から未記入の給与貸方を
補完して、記帳済み給与を暦年で集計します。株価と為替による円換算、
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

株式単位と数量のscaleは、既存の帳簿設定で定義します。このパッケージは
数量のscaleや取得費を推定しません。給与科目はこの運用専用とし、通常給与や
その他の収入を混在させないでください。

原資料から認識日と円換算額を確認し、その結果を明示的に記帳します。
例えば100株・1株100ドル・1ドル150円という確認済みの評価額は150万円です。
本パッケージは株価・為替の観測や計算を再検証しません。原資料と計算根拠を
`raw/`に保存し、通常の添付参照も記録してください。`valuation_source`は
資料の参照先であり、添付内容のハッシュ化や真正性の証明ではありません。

株式借方と給与貸方に、同一の権利確定情報を記録します。

```yaml
lines:
  - account: Assets:AMZN
    debit: 1500000
    quantity: 100
    unit: AMZN
    jp_rsu: &vesting
      event_id: amazon-2026-05
      grant_id: grant-1
      payer: Amazon.com Inc.
      recognition_date: '2026-05-01'
      gross_jpy: 1500000
      valuation_source: raw/vesting-2026-05.pdf
  - account: Income:RSU
    credit: null
    jp_rsu: *vesting
```

仕訳日と`recognition_date`を一致させ、`iris journal complete`で給与貸方を
プレビューします。通常のrevision確認付き操作で適用してください。
既存の貸借補完を使うため、株式の借方金額は入力済みである必要があります。
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
