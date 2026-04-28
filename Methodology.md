# 📑 Research Methodology & Technical Appendix

---

## 1. Data Source & Longitudinal Scope
This study utilizes a comprehensive longitudinal dataset constructed from the **State Bank of Pakistan (SBP)** annual publications: *“Financial Statements Analysis of All Listed Non-Financial Companies.”*

* **Sample Period:** 2005 – 2023 (19 Years)
* **Target Population:** All non-financial firms listed on the Pakistan Stock Exchange (PSX).
* **Unit of Analysis:** Firm-year observations.

---

## 2. Multi-Period Schema Integration
A significant challenge in this research was the evolution of SBP reporting standards. The SBP revised its data hierarchy and formula brackets across three distinct eras. This study developed specialized computational pipelines to map these shifting schemas into a unified dataset:

### 🗓️ Period 1: 2005 – 2008
* **Schema Type:** Legacy SBP format.
* **Strategy:** Direct extraction of primary aggregates and sub-component sums.

### 🗓️ Period 2: 2009 – 2013
* **Schema Type:** Transitional format.
* **Strategy:** Re-anchoring of liability variables to account for expanded reporting categories.

### 🗓️ Period 3: 2014 – 2023
* **Schema Type:** Modern IFRS-aligned format.
* **Strategy:** Implementation of a **Fuzzy-Logic Matching Engine** to handle dynamic variable sub-brackets.

---

## 3. Variable Operationalization
The following formulas were applied consistently across all reporting eras to ensure longitudinal reliability.

### 📈 Profitability Metric
> **Return on Assets (ROA)**
> Measures how efficiently a firm uses its assets to generate net earnings.
$$ROA = \frac{\text{Profit After Tax}}{\text{Total Assets}}$$

### ⚖️ Shariah Screening Ratios
> **Debt Ratio (DR)**
> Evaluates the level of interest-bearing debt relative to total assets.
$$DR = \frac{\text{Long-Term Debt} + \text{Short-Term Borrowings}}{\text{Total Assets}}$$

> **Investment Ratio (IR)**
> Assesses the proportion of non-compliant (interest-bearing) investments.
$$IR = \frac{\text{Short-Term Investments}}{\text{Total Assets}}$$

> **Income Ratio (IncR)**
> Captures the percentage of non-permissible (other) income.
$$IncR = \frac{\text{Non-Compliant (Other) Income}}{\text{Total Sales}}$$

> **Illiquid Asset Ratio (IAR)**
> Determines the ratio of physical or "real" assets to total assets.
$$IAR = \frac{\text{Non-Current Assets} + \text{Inventories}}{\text{Total Assets}}$$

> **Net Liquid Assets (NLA)**
> A strict liquidity measure relative to share capital.
$$NLA = \frac{\text{Total Assets} - \text{Illiquid Assets} - \text{Total Liabilities}}{\text{Total Number of Outstanding Shares}}$$

---

## 4. Computational Logic & Cleaning

### 🔍 Fuzzy-Logic Variable Matching
Because the SBP frequently updated the internal formulas in their spreadsheets (e.g., changing `(A2+A3)` to `(A1+A3+A4+A5+A6)`), a standard cell-reference approach would fail. 
* **Solution:** The Python pipeline utilizes a **root-string search algorithm**. This engine scans for the semantic core of a variable (e.g., "Non-Current Assets") rather than the exact string, ensuring data continuity across 19 years.

### 🛡️ Null-Safe Arithmetic ("Safe Addition")
In financial data, a blank entry often represents zero exposure. Standard code often treats `Value + Null` as `Null`, leading to missing data.
* **Solution:** A custom `safe_add` function was implemented to treat null values as $0$ for additions, while maintaining strict `null` status for divisions to prevent division-by-zero errors.

### 🧹 Data Normalization Parser
Raw data underwent the following transformations to become "Model-Ready":
1.  **Parentheses to Negative:** Converted accounting notation `(500)` to `-500.0`.
2.  **String Sanitization:** Removed commas, thousand-separators, and non-breaking spaces.
3.  **Percentage Conversion:** Automatically divided string-based percentages (e.g., `"5.5%"`) by 100.

---

## 5. Sequence & Hierarchy Preservation
To maintain the economic context of the PSX, this study avoids alphabetical sorting which disrupts industry-specific hierarchies. 

* **Strategy:** The dataset utilizes **Categorical Sequencing**. 
* **Benefit:** The final master file adheres to the original SBP Sector/Sub-Sector order, allowing for nuanced industry-wise comparative analysis.

---
*This methodology document serves as the technical foundation for the empirical findings presented in this thesis.*
