# Shariah Compliance and Firm Profitability Analysis (2005-2023)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-green)
![Google Colab](https://img.shields.io/badge/Environment-Google%20Colab-orange)

## 📌 Project Overview
This repository contains the data processing pipeline and analytical codebase for the thesis: **"The Impact of Shariah Screening Compliance on Firms’ Profitability: Empirical Evidence from Pakistan."**

The objective of this project is to automate the extraction, normalization, and computation of strict Islamic financial screening ratios for non-financial companies listed on the Pakistan Stock Exchange (PSX). The data spans a 19-year period (2005–2023) and is sourced from the State Bank of Pakistan's (SBP) financial statement analysis.

## 📊 Data Source & Challenges
The primary dataset is the **SBP Financial Statements Analysis of All Listed Non-Financial Companies (2005-23).xlsx**. 

Because the SBP periodically updates its accounting standards and line-item classifications (IFRS adoption, reporting hierarchy changes), the data is split into three distinct historical periods with varying schemas:
1. `2005-08`
2. `2009-13`
3. `2014-23`

This codebase utilizes **dynamic fuzzy-matching algorithms** and **null-safe mathematical functions** to seamlessly bridge these schema changes without breaking the calculations.

## 🧮 Computed Variables
The Python scripts process the raw financial data to calculate the following Shariah-compliance criteria and profitability metrics:

| Variable | Description | Definition / Formula |
| :--- | :--- | :--- |
| **ROA** | Return on Assets | Profit / Average Total Assets |
| **DR** | Debt Ratio | (Long Term Debt + Short Term Borrowings) / Total Assets |
| **IR** | Investment Ratio | Short Term Investments / Total Assets |
| **IncR** | Income Ratio | Non-Compliant (Other) Income / Total Sales |
| **IAR** | Illiquid Asset Ratio | (Non-Current Assets + Inventory) / Total Assets |
| **NLA** | Net Liquid Assets | (Total Assets - Illiquid Assets - Total Liabilities) / Total Shares |

## 📁 Repository Structure

```text
├── data/
│   ├── raw/
│   │   └── 2005-23.xlsx                 # Original SBP dataset (Not included due to size/limits)
│   ├── processed/
│   │   ├── computed_variables_2005_08.csv
│   │   ├── computed_variables_2009_13.csv
│   │   ├── computed_variables_2014_23.csv
│   │   └── computed_variables_2005_23_
