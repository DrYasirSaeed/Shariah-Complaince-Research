"""
data_extraction.py
------------------
Reads each period-specific sheet from the SBP Excel workbook and computes
Shariah-compliance ratios and control variables for every company-year pair.

Usage
-----
    from src.data_extraction import process_shariah_data, run_all_periods

    # Process a single sheet
    df = process_shariah_data(
        excel_file_path="data/2005-23.xlsx",
        sheet_name="2005-08",
        output_csv_path="data/01_computed_variables_2005_08.csv",
        years_map={"2005": 4, "2006": 5, "2007": 6, "2008": 7},
        item_name_mappings=ITEM_MAPPINGS_05_08,
    )

    # Or process all periods at once
    run_all_periods(excel_file_path="data/2005-23.xlsx", output_dir="data/")
"""

import pandas as pd
from src.utils import normalize_item, parse_num, safe_div, safe_add, get_item_year_value

# ---------------------------------------------------------------------------
# Aggregate sector labels that are NOT real companies and must be filtered out
# ---------------------------------------------------------------------------
AGGREGATE_SECTORS = {
    '703 - All Sector',
    '704 - Textile Sector',
    '705 - Coke and Refined Petroleum Products',
    '706 - Chemicals, Chemical Products and Pharmaceuticals',
    '707 - Electrical Machinery and Apparatus',
    '709 - Paper, Paperboard and Products',
    '710 - Fuel and Energy Sector',
    '711 - Information and Communication Services',
    '712 - Manufacturing',
    '714 - Motor Vehicles, Trailers & Autoparts',
    '715 - Other Services Activities',
    '723 - Spinning, Weaving, Finishing of Textiles',
    '724 - Made-up textile articles',
    '725 - Other textiles n.e.s.',
    '726 - Sugar',
    '727 - Food',
    '728 - Mineral products',
    '729 - Cement',
    'Sectors',
    'Sub-sector',
}

# ---------------------------------------------------------------------------
# Per-period item-name mappings
# ---------------------------------------------------------------------------
ITEM_MAPPINGS_05_08 = {
    'A':      "A. Non-Current Assets (A2+A3)",
    'B':      ["B. Current Assets (B1+B2+B3+B4+B5)",
               "B. Current Assets (B1+B2+B3+B4+B5+B6)"],
    'TotalAB':"Total Assets (A+B) / Equity & Liabilities (C+D+E)",
    'D':      "D. Non-Current Liabilities (D1+D2)",
    'E':      "E. Current Liabilities (E1+E2)",
    'STB':    ["1. Short term borrowings",
               "of which: i) Short term secured loans"],
    'B2':     "2. Inventories",
    'B4':     "4. Short term investments",
    'F1':     "1. Sales",
    'F5':     "5. Other income / (loss)",
    'C1':     "1. Issued, Subscribed & Paid up capital",
    'ROA':    ["P3. Return on Assets (F7 as a % of Avg {Current year(A+B),previous year (A+B)}",
               "P3. Return on Assets (F7 as a % of Avg {Current year(A+B),previous year (A+B)})",
               "Return on Assets"],
}

ITEM_MAPPINGS_09_13 = {
    'A':      ["A. Non-Current Assets (A1+A3+A4+A5+A6)",
               "A. Non-Current Assets (A2+A3)"],
    'B':      ["B. Current Assets (B1+B2+B3+B4+B5)",
               "B. Current Assets (B1+B2+B3+B4+B5+B6)"],
    'TotalAB':"Total Assets (A+B) / Equity & Liabilities (C+D+E)",
    'D':      ["D. Non-Current Liabilities (D1+D2+D3+D4)",
               "D. Non-Current Liabilities (D1+D2)"],
    'E':      "E. Current Liabilities (E1+E2)",
    'STB':    ["1. Short term borrowings",
               "of which: i) Short term secured loans"],
    'B2':     "2. Inventories",
    'B4':     "4. Short term investments",
    'F1':     "1. Sales",
    'F5':     "5. Other income / (loss)",
    'C1':     "1. Issued, Subscribed & Paid up capital",
    'ROA':    "Return on Assets",
}

ITEM_MAPPINGS_14_23 = {
    'A':      "A. Non-Current Assets",
    'B':      "B. Current Assets",
    'TotalAB':"Total Assets",
    'D':      "D. Non-Current Liabilities",
    'E':      "E. Current Liabilities",
    'STB':    ["1. Short term borrowings",
               "Short term borrowings",
               "Short term secured loans"],
    'B2':     ["2. Inventories", "Inventories"],
    'B4':     ["4. Short term investments", "Short term investments"],
    'F1':     ["1. Sales", "Sales"],
    'F5':     ["5. Other income", "Other income"],
    'C1':     ["1. Issued, Subscribed & Paid up capital",
               "Issued, Subscribed & Paid up capital"],
    'ROA':    "Return on Assets",
}


# ---------------------------------------------------------------------------
# Core extraction function
# ---------------------------------------------------------------------------

def process_shariah_data(
    excel_file_path: str,
    sheet_name: str,
    output_csv_path: str,
    years_map: dict,
    item_name_mappings: dict,
) -> pd.DataFrame:
    """
    Extract financial data from one sheet and compute Shariah-compliance
    variables plus control variables for every company-year observation.

    Args:
        excel_file_path:    Path to the source Excel workbook.
        sheet_name:         Worksheet name (e.g. '2005-08').
        output_csv_path:    Destination CSV path for computed variables.
        years_map:          {year_label: col_index} mapping (0-based).
        item_name_mappings: {internal_key: name_or_list_of_names} mapping.

    Returns:
        DataFrame with one row per (company, year).
    """
    print(f"\nLoading sheet '{sheet_name}' from {excel_file_path} …")
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=None)

    data: dict = {}
    ordered_companies: list = []
    company_metadata: dict = {}

    print("Parsing rows …")
    for _, row in df.iloc[1:].iterrows():
        sector_raw    = row[0]
        subsector_raw = row[1]
        company_raw   = row[2]
        item_raw      = row[3]

        company = str(company_raw).strip() if pd.notna(company_raw) else ""
        item    = normalize_item(item_raw)

        if not company or not item:
            continue
        if company in AGGREGATE_SECTORS:
            continue

        if company not in data:
            data[company] = {}
            ordered_companies.append(company)
            company_metadata[company] = {
                'Sector':     str(sector_raw).strip()    if pd.notna(sector_raw)    else "",
                'Sub-Sector': str(subsector_raw).strip() if pd.notna(subsector_raw) else "",
            }

        if item not in data[company]:
            data[company][item] = {}

        for year_label, col_idx in years_map.items():
            if col_idx < len(row):
                cell_val = row[col_idx]
                data[company][item][year_label] = (
                    float(cell_val)
                    if isinstance(cell_val, (int, float))
                    else parse_num(cell_val)
                )
            else:
                data[company][item][year_label] = None

    print("Computing variables …")
    results = []

    for company in ordered_companies:
        cm   = data[company]
        meta = company_metadata[company]

        for yr in years_map:
            m = item_name_mappings

            A      = get_item_year_value(cm, m['A'],      yr)
            B      = get_item_year_value(cm, m['B'],      yr)
            D      = get_item_year_value(cm, m['D'],      yr)
            E      = get_item_year_value(cm, m['E'],      yr)
            STB    = get_item_year_value(cm, m['STB'],    yr)
            B2     = get_item_year_value(cm, m['B2'],     yr)
            B4     = get_item_year_value(cm, m['B4'],     yr)
            F1     = get_item_year_value(cm, m['F1'],     yr)
            F5     = get_item_year_value(cm, m['F5'],     yr)
            C1     = get_item_year_value(cm, m['C1'],     yr)
            ROA    = get_item_year_value(cm, m['ROA'],    yr)

            TotalAB = get_item_year_value(cm, m['TotalAB'], yr)
            if TotalAB is None:
                TotalAB = safe_add(A, B)

            I2 = (C1 / 10.0) if C1 is not None else None

            if ROA is not None and abs(ROA) > 1:
                ROA = ROA / 100.0

            # --- Ratios ---
            DR   = safe_div(safe_add(D, STB), TotalAB)
            IR   = safe_div(B4, TotalAB)
            IncR = safe_div(F5, F1)
            IAR  = safe_div(safe_add(A, B2), TotalAB)

            illiquid  = safe_add(A, B2)
            NLA_total = None
            if all(v is not None for v in [TotalAB, illiquid, D, E]):
                NLA_total = TotalAB - illiquid - (D + E)
            NLA = safe_div(NLA_total, I2)

            Tangibility = safe_div(A, TotalAB)

            def _fmt(v):
                return round(v, 6) if v is not None else ""

            results.append({
                'Sector':             meta['Sector'],
                'Sub-Sector':         meta['Sub-Sector'],
                'Company':            company,
                'Year':               int(yr),
                'ROA':                _fmt(ROA),
                'DR':                 _fmt(DR),
                'IR':                 _fmt(IR),
                'IncR':               _fmt(IncR),
                'NLA':                _fmt(NLA),
                'IAR':                _fmt(IAR),
                'Firm Size':          _fmt(TotalAB),
                'Tangibility':        _fmt(Tangibility),
                'Sales':              _fmt(F1),
                'Non_Current_Assets': _fmt(A),
                'Total_Assets':       _fmt(TotalAB),
            })

    out_df = pd.DataFrame(results)
    out_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"Saved {len(out_df):,} rows → {output_csv_path}")
    return out_df


# ---------------------------------------------------------------------------
# Convenience runner for all three periods
# ---------------------------------------------------------------------------

def run_all_periods(excel_file_path: str, output_dir: str) -> dict:
    """
    Process all three time periods and save individual CSVs.

    Args:
        excel_file_path: Path to the source workbook.
        output_dir:      Directory where CSVs will be saved.

    Returns:
        Dict of {period_label: DataFrame}.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    periods = [
        ("2005-08",
         {"2005": 4, "2006": 5, "2007": 6, "2008": 7},
         ITEM_MAPPINGS_05_08,
         "01_computed_variables_2005_08.csv"),
        ("2009-13",
         {"2009": 4, "2010": 5, "2011": 6, "2012": 7, "2013": 8},
         ITEM_MAPPINGS_09_13,
         "02_computed_variables_2009_13.csv"),
        ("2014-23",
         {"2014": 4, "2015": 5, "2016": 6, "2017": 7, "2018": 8,
          "2019": 9, "2020": 10, "2021": 11, "2022": 12, "2023": 13},
         ITEM_MAPPINGS_14_23,
         "03_computed_variables_2014_23.csv"),
    ]

    dfs = {}
    for sheet, years_map, mappings, fname in periods:
        out_path = os.path.join(output_dir, fname)
        dfs[sheet] = process_shariah_data(
            excel_file_path=excel_file_path,
            sheet_name=sheet,
            output_csv_path=out_path,
            years_map=years_map,
            item_name_mappings=mappings,
        )

    return dfs
