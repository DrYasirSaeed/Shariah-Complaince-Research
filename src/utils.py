"""
utils.py
--------
Shared helper functions used across the Shariah Compliance pipeline.
"""

import re
import pandas as pd


def normalize_item(s) -> str:
    """
    Clean and normalize a string value by collapsing internal whitespace.

    Args:
        s: Raw string or value (may be NaN).

    Returns:
        Stripped, single-space-normalized string, or "" for NaN/None.
    """
    if pd.isna(s):
        return ""
    return re.sub(r'\s+', ' ', str(s)).strip()


def parse_num(s):
    """
    Parse a string into a float, handling commas, percentages, and
    parenthesised negative values (e.g. "(1,234.56)").

    Args:
        s: Raw string or numeric value.

    Returns:
        Float, or None if parsing fails or the value is blank/missing.
    """
    if pd.isna(s):
        return None
    t = str(s).strip()
    if t in ("-", "N/A", ""):
        return None

    neg = False
    if t.startswith('(') and t.endswith(')'):
        neg = True
        t = t[1:-1].strip()

    is_percent = '%' in t
    t = t.replace(',', '').replace('%', '')

    try:
        n = float(t)
        if neg:
            n = -n
        if is_percent:
            n = n / 100.0
        return n
    except ValueError:
        return None


def safe_div(a, b):
    """
    Divide a by b, returning None when division is undefined or inputs are invalid.

    Args:
        a: Numerator.
        b: Denominator.

    Returns:
        a / b as float, or None.
    """
    if a is None or b is None or pd.isna(a) or pd.isna(b) or b == 0.0:
        return None
    return a / b


def safe_add(*args):
    """
    Sum valid (non-None, non-NaN) values.

    Args:
        *args: Any number of numeric values or None/NaN.

    Returns:
        Sum of valid values as float, or None if no valid values exist.
    """
    valid = [a for a in args if a is not None and not pd.isna(a)]
    if not valid:
        return None
    return sum(valid)


def get_item_year_value(company_map: dict, item_names, year: str):
    """
    Retrieve a financial item's value for a given year from a company's data map.

    Matching strategy:
      1. Exact match against every candidate name.
      2. Case-insensitive partial match (handles bracket variations, e.g.
         "D. Non-Current Liabilities" inside
         "D. Non-Current Liabilities (D1+D2+D3+D4+D5)").

    Args:
        company_map: {item_name: {year_str: value}} dict for one company.
        item_names:  Single string or list of possible item name strings.
        year:        Year label string (e.g. "2009").

    Returns:
        Matched value (float or None), or None if not found.
    """
    if isinstance(item_names, str):
        item_names = [item_names]

    # 1. Exact match
    for name in item_names:
        if name in company_map and year in company_map[name]:
            return company_map[name][year]

    # 2. Partial / fuzzy match
    for name in item_names:
        for key in company_map:
            if str(name).lower() in str(key).lower():
                val = company_map[key].get(year)
                if val is not None:
                    return val

    return None
