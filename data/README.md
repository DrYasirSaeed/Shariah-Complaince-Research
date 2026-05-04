# Data Directory

This directory holds the source Excel file and all intermediate/final CSVs
produced by the pipeline.  **Raw data files are excluded from version control**
via `.gitignore` to avoid committing large or proprietary files.

## Source file

Place `2005-23.xlsx` here (or update the path in the notebook / scripts).

## Generated files (pipeline outputs)

| File | Step | Description |
|------|------|-------------|
| `01_computed_variables_2005_08.csv` | 1 | Variables for 2005–2008 |
| `02_computed_variables_2009_13.csv` | 2 | Variables for 2009–2013 |
| `03_computed_variables_2014_23.csv` | 3 | Variables for 2014–2023 |
| `04_computed_variables_2005_23_Combined.csv` | 4 | Combined panel + Sales Growth |
| `05_Winsorized_Data.csv` | 5 | After 1%–99% winsorization |
| `06_Cleaned_Panel_Data.csv` | 6 | After sector harmonization |
| `07_Log_Transformed_Data.csv` | 7 | Firm Size log-transformed (analysis-ready) |

`07_Log_Transformed_Data.csv` is the final input for all econometric and
clustering analyses.
