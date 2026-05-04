# Shariah Compliance Project: Data Analysis and Econometric Modeling

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive pipeline for extracting, processing, and analyzing Shariah-compliance variables from Pakistani non-financial corporate (NFC) financial data spanning 2005–2023. The project covers everything from raw Excel ingestion to panel econometrics and K-Means clustering.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Setup and Installation](#setup-and-installation)
- [Pipeline Walkthrough](#pipeline-walkthrough)
- [Variables](#variables)
- [Key Results](#key-results)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

This project processes multi-year financial statement data from the State Bank of Pakistan (SBP) to compute Shariah-compliance ratios and control variables. The pipeline then applies rigorous econometric techniques — including panel unit root tests, Hausman test, and Fixed Effects regression — as well as unsupervised machine learning (K-Means clustering) to identify firm archetypes.

### Research Questions

1. What is the level of Shariah compliance among Pakistani non-financial corporations over 2005–2023?
2. How do Shariah-compliance indicators relate to firm profitability (ROA)?
3. Can firms be meaningfully clustered into distinct Shariah-compliance archetypes?

---

## Repository Structure

```
shariah-compliance-project/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/                          # Modular Python source code
│   ├── __init__.py
│   ├── data_extraction.py        # Excel parsing and variable calculation
│   ├── data_cleaning.py          # Winsorization, harmonization, log transforms
│   ├── econometrics.py           # Unit root tests, Hausman, Fixed Effects
│   ├── clustering.py             # K-Means clustering and archetype analysis
│   └── utils.py                  # Shared helper functions
│
├── notebooks/                    # Jupyter notebooks (exploratory / presentation)
│   └── Shariah_Compliance_with_Control_variables.ipynb
│
├── data/                         # Data directory (source files not tracked in Git)
│   ├── .gitkeep
│   └── README.md
│
├── results/                      # Output reports and figures (not tracked)
│   └── .gitkeep
│
└── docs/
    └── methodology.md            # Detailed methodology notes
```

---

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- A Google Colab environment (recommended) or a local Jupyter environment
- Source Excel file: `2005-23.xlsx` placed in the `data/` directory (or Google Drive path configured in notebooks)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or in Google Colab:

```python
!pip install linearmodels shap kneed python-docx
```

---

## Pipeline Walkthrough

The pipeline consists of numbered stages, each producing a CSV or Word document:

| Step | Script / Notebook Cell | Output File |
|------|------------------------|-------------|
| 1 | `data_extraction.py` → `process_shariah_data()` | `01_computed_variables_2005_08.csv` |
| 2 | `data_extraction.py` → `process_shariah_data()` | `02_computed_variables_2009_13.csv` |
| 3 | `data_extraction.py` → `process_shariah_data()` | `03_computed_variables_2014_23.csv` |
| 4 | `data_cleaning.py` → combine & sales growth | `04_computed_variables_2005_23_Combined.csv` |
| 5 | `data_cleaning.py` → winsorization | `05_Winsorized_Data.csv` |
| 6 | `data_cleaning.py` → sector harmonization | `06_Cleaned_Panel_Data.csv` |
| 7 | `data_cleaning.py` → log transform firm size | `07_Log_Transformed_Data.csv` |
| 8 | `econometrics.py` → unit root tests | `06_unit_root_test_report.docx` |
| 9 | `econometrics.py` → optimal lag selection | `07_optimal_lag_selection_report.docx` |
| 10 | `econometrics.py` → Hausman test | `08_hausman_test_report.docx` |
| 11 | `econometrics.py` → Fixed Effects regression | `09_fixed_effects_regression_report.docx` |
| 12 | `clustering.py` → K-Means clustering | `11_kmeans_clustering_report_k4.docx` |

---

## Variables

### Shariah-Compliance Indicators

| Variable | Description | Formula |
|----------|-------------|---------|
| `DR` | Debt Ratio | `(Non-Current Liabilities + Short-Term Borrowings) / Total Assets` |
| `IR` | Investment Ratio | `Short-Term Investments / Total Assets` |
| `IncR` | Income Ratio | `Other Income / Sales` |
| `IAR` | Illiquid Asset Ratio | `(Non-Current Assets + Inventories) / Total Assets` |
| `NLA` | Net Liquid Assets per Share | `(Total Assets − Illiquid Assets − Total Liabilities) / Shares` |

### Control Variables

| Variable | Description |
|----------|-------------|
| `ROA` | Return on Assets (dependent variable) |
| `Log Firm Size` | Natural log of Total Assets |
| `Tangibility` | Non-Current Assets / Total Assets |
| `Sales Growth` | Year-over-year % change in Sales |

---

## Key Results

- **Optimal Lag:** Lag 0 (contemporaneous relationships dominate)
- **Panel Model:** Fixed Effects (Hausman test rejected Random Effects)
- **Clustering:** K = 4 clusters identified via Elbow and Silhouette methods
- **Stationarity:** All variables confirmed stationary (I(0)) via Fisher-ADF panel unit root tests

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
