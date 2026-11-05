# Japan

**English** | [日本語](README.ja.md)

The packages in this folder add Japanese rules to an IrisBooks Book. The engine
itself is region-agnostic: double entry, journals, assets, recipes and filings
work the same in every region. Japanese consumption tax, depreciation methods,
small-asset deductions and share-compensation rules come only from the packages
you select, and statutory forms are prepared by you or your AI from the figures
they produce.

## Set up a Japanese book

`iris init --region JP` keeps the book's dates in Japan time and defaults the
currency to JPY. The Japanese starter charts come in `--chart general`, `it`
and `food`; their owner accounts, 事業主貸 and 事業主借, are marked
`owner: true`, so they keep the balance-sheet layout the 青色申告決算書 expects
and stay out of Net Worth. Business setup (the default `--preset`) selects the
common packages plus jp-tax-classification, jp-tax-amount, jp-tax-filing,
jp-small-asset-deduction and jp-declining-balance; turn off what does not apply
with `iris overlay select`.

## Choose packages

| Your situation | Select |
|---|---|
| 免税事業者: no consumption-tax return | None of the consumption-tax packages. Record tax-inclusive amounts as ordinary sales and expenses. |
| 課税事業者: classify each taxable line | [jp-tax-classification](jp-tax-classification/README.md) |
| 税抜経理: propose missing tax amounts | Add [jp-tax-amount](jp-tax-amount/README.md) |
| Prepare the 消費税 return figures | Add [jp-tax-filing](jp-tax-filing/README.md) |
| 定率法 depreciation | [jp-declining-balance](jp-declining-balance/README.md) |
| 少額減価償却資産 immediate deduction | [jp-small-asset-deduction](jp-small-asset-deduction/README.md) |
| RSU vesting, listed shares, USD cash | [jp-rsu](jp-rsu/README.md), [jp-securities-basis](jp-securities-basis/README.md), [jp-foreign-currency](jp-foreign-currency/README.md) |

Select every dependency explicitly; see
[Use packages in a Book](../README.md#use-packages-in-a-book). Each package's
README links its workflow guide.

## Look up figures no package ships

Some figures depend on the asset, the taxpayer, the municipality or this year's
form, so no package ships them. Look them up on the current National Tax Agency
(NTA) or municipality pages and record the resolved value in the Book, where
your 税理士 can check it:

- **Useful life (耐用年数).** 耐用年数省令 別表第一 (general assets) and
  別表第二 (machinery and equipment), on the
  [NTA's useful-life pages](https://www.nta.go.jp/law/joho-zeikaishaku/hojin/sintaiyo/menu.htm),
  recorded as `useful_life_months` on the asset file. Record the classification
  you used as `yotaikai_class`; if it is unclear, ask what the asset is.
- **定率法 rates.** 償却率, 保証率 and 改定償却率 from 別表第十: the 200% table
  for acquisitions from 2012-04-01, the 250% table for 2007-04-01 through
  2012-03-31. An asset keeps the table it was acquired under. Pass the rates to
  jp-declining-balance.
- **みなし仕入率 for 簡易課税.** Passed to jp-tax-filing as `deemed_pct`.

## Record the year's details

- **Receipts.** Keeping each receipt as its own line is a working policy. For
  白色申告 bookkeeping the NTA also describes recording daily totals
  ([No.2080](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2080.htm)).
- **Business-use share (家事按分).** Household-related costs need records that
  distinguish the business portion
  ([No.2210](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2210.htm));
  `iris allocation` splits a charge by the fraction you confirm.
- **Fund units.** Repeated purchases have a statutory acquisition-cost method
  ([No.1464](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1464.htm));
  a FIFO or moving-average label in the book is a management choice, not a tax
  determination. Funds quote 基準価額 per 10,000 units. For a NISA account,
  confirm the broker's account classification, the
  [FSA's NISA rules](https://www.fsa.go.jp/policy/nisa2/know/index.html) and the
  [current eligible products](https://www.fsa.go.jp/policy/nisa2/products/).
- **Small assets written off at once.** Book the purchase to the asset account
  and let `iris asset depreciate` write it off; booking it as an expense too
  counts it twice. Whether a small item gets an asset file at all is the owner's
  call. 一括償却資産 (`toku_rei: ikkatsu_3yr`) is unsupported: keep the evidence
  and record the treatment in `notes/open-questions.md`.
- **Disposals.** Set the disposal-year row of a recorded schedule to the months
  held (月割), and book the difference between proceeds and the carrying amount
  to 固定資産売却益, 固定資産売却損 or 除却損.

## File the returns

IrisBooks sums; you or your AI prepare the forms, and you file them. Work from the engine's figures and the
recorded filings plus this year's official form, and keep prepared forms in the
Book under `compiled/jp/<form>/`.

- **消費税.** The 課税期間 is the calendar year for an individual and the fiscal
  year for a corporation. jp-tax-filing's figures exclude the national/local
  (国税/地方税) split and the rounding of the 課税標準額 down to ¥1,000; apply
  them from the recorded figures. On a 税抜経理 Book, book the amount
  jp-tax-amount proposes on 仮払消費税 / 仮受消費税.
- **固定資産台帳 and 別表16.** Use the asset files with `iris export assets --year`
  and `iris asset schedule --year`. Take `opening_nbv`, `period_dep`,
  `closing_nbv`, `accumulated` and `disposal_nbv` from the CSV rather than
  recomputing them.
- **償却資産税 (per municipality).** A calendar-year return for every fiscal
  year: the assessment date is January 1 and the return is due January 31. The
  評価額 comes from the acquisition cost and the 減価残存率 table, not from
  `closing_nbv`. Items written off under `toku_rei: shoutoku_300k` are still
  declared.

## Keep the records

The server's correction/deletion history is what Japanese rules call the
訂正・削除の履歴. Keep the books for the statutory retention period: 7 years, up
to 10 in some corporate cases. IrisBooks holds no certification (for example, no JIIMA 認証)
and does not claim that a Book kept in it meets the 優良電子帳簿 requirements.
Whether your books qualify, and any advance notification (届出) to your tax
office, is for you and your 税理士 to decide.
