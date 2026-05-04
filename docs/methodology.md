# Methodology Notes

## 1. Data Source

The primary data source is a multi-sheet Excel workbook (`2005-23.xlsx`)
containing financial statements for Pakistani non-financial corporations (NFCs)
as published by the State Bank of Pakistan (SBP).  Three period-specific
worksheets are processed: **2005-08**, **2009-13**, and **2014-23**.

---

## 2. Data Extraction Challenges

Each sheet uses slightly different item naming conventions:

| Period | Key naming feature |
|--------|--------------------|
| 2005–08 | Exact, compact names (`A. Non-Current Assets (A2+A3)`) |
| 2009–13 | Some items renamed; lists of aliases used |
| 2014–23 | Bracket suffixes removed; fuzzy substring matching required |

The `get_item_year_value` function resolves this with a two-pass strategy:
exact match first, then case-insensitive partial match.

---

## 3. Variable Definitions

### Shariah-Compliance Indicators

| Symbol | Variable | Numerator | Denominator |
|--------|----------|-----------|-------------|
| DR | Debt Ratio | Non-Current Liabilities + Short-Term Borrowings | Total Assets |
| IR | Investment Ratio | Short-Term Investments | Total Assets |
| IncR | Income Ratio | Other Income | Sales |
| IAR | Illiquid Asset Ratio | Non-Current Assets + Inventories | Total Assets |
| NLA | Net Liquid Assets/Share | Total Assets − Illiquid Assets − Total Liabilities | Shares in issue |

### Control Variables

| Symbol | Variable | Notes |
|--------|----------|-------|
| ROA | Return on Assets | Dependent variable; converted from % if > 1 |
| Log Firm Size | ln(Total Assets) | Non-positive values → NaN |
| Sales Growth | YoY % change in Sales | Infinite and zero-sales values → NaN |
| Tangibility | Non-Current Assets / Total Assets | Dropped due to VIF with IAR |

---

## 4. Data Treatment

### Winsorization
All continuous variables are winsorized at the **1st and 99th percentiles**
to limit extreme outlier influence without discarding observations.

### Sector Harmonisation
- `'Food'` → `'Food Products'` (label standardisation).
- `'Goodluck Industries Ltd.'` reclassified to Food Products for 2005–2013.
- Aggregate sector rows removed (`727 - Food Products`, etc.).

---

## 5. Econometric Strategy

1. **Panel Unit Root Tests (Fisher-ADF)** — confirm stationarity (I(0)) for
   all variables before regression.
2. **Optimal Lag Selection** — PanelOLS within R² and RandomForest test MSE
   both favour **Lag 0**.
3. **Hausman Test** — rejects Random Effects; **Fixed Effects** model selected.
4. **Fixed Effects Regression** — entity-demeaned PanelOLS with clustered
   standard errors where applicable.
5. **Sector-Wise FE** — sectors with ≥ 15 unique companies and ≥ 50
   observations analysed independently.

---

## 6. Clustering

K-Means clustering on company-level means of
`[ROA, DR, IAR, IncR, NLA, Log Firm Size]`.

- **Elbow Method** (KneeLocator) and **Silhouette Score** jointly identify
  **K = 4** as optimal.
- PCA reduces the feature space to 2D for visualisation.
- Cluster archetypes labelled by mean ROA (descending).

---

## 7. Notes on IR (Investment Ratio)

IR is typically sparse (many firms hold no short-term investments).
In regression models a **binary dummy** (`IR_Dummy = 1 if IR > 0`) is used
to capture the threshold effect aligned with KMI-30 screening rules.
