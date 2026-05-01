import pandas as pd
import numpy as np
from google.colab import drive

# 1. Mount Google Drive
# This step connects your Google Colab environment to your Google Drive,
# allowing the script to access files stored there.
drive.mount('/content/drive')

# 2. File Paths
# Define the base path and the paths to the three CSV files generated in previous steps,
# as well as the output path for the final combined CSV.
base_path = '/content/drive/MyDrive/Github-Cursor/Shariah Compliance Project/Extracted Data/'

file1 = base_path + '01_computed_variables_2005_08.csv'
file2 = base_path + '02_computed_variables_2009_13.csv'
file3 = base_path + '03_computed_variables_2014_23.csv'
out_file = base_path + '04_computed_variables_2005_23_Combined.csv'

print("Loading the three CSV files...")
# Load the dataframes from the individual CSV files.
# A try-except block is used to gracefully handle cases where a file might be missing.
try:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df3 = pd.read_csv(file3)
except FileNotFoundError as e:
    print(f"Error finding file: {e}")
    print("Please make sure all three scripts have been successfully run first.")
    raise

# --- Debugging: Print head of each DataFrame after loading ---
print("\nPreview of df1 (2005-08 data):")
display(df1.head())
print("\nPreview of df2 (2009-13 data):")
display(df2.head())
print("\nPreview of df3 (2014-23 data):")
display(df3.head())
# --- End Debugging ---

# 3. Combine all rows into one massive dataset
print("Concatenating files...")
# Use pd.concat to stack the three DataFrames vertically.
# 'ignore_index=True' resets the index for the combined DataFrame.
df_combined = pd.concat([df1, df2, df3], ignore_index=True)

# 4. Extract the exact original top-to-bottom sequence of companies from File 1
# This step ensures that the final sorted output maintains the company order as it appeared in the original Excel file.
# drop_duplicates() preserves the first time it sees each company, effectively keeping the original Excel sequence intact.
original_company_sequence = df1['Company'].drop_duplicates().tolist()

# (Safety Check): If any new companies appeared in 2009-13 or 2014-23 that weren't in 2005-08,
# append them to the end of our sequence list so they aren't lost in the sorting.
all_unique_companies = df_combined['Company'].drop_duplicates().tolist()
for company in all_unique_companies:
    if company not in original_company_sequence:
        original_company_sequence.append(company)

print("Sorting by Original Company Sequence, then chronologically by Year...")
# 5. Convert the 'Company' column into a Categorical data type with our custom sequence
# This is a key step for custom sorting. By making 'Company' a categorical type with a defined order,
# Pandas will sort based on this order rather than alphabetical order.
df_combined['Company'] = pd.Categorical(
    df_combined['Company'],
    categories=original_company_sequence,
    ordered=True
)

# 6. Sort! Because 'Company' is categorical, it will sort by your Excel order, then by Year
# The inplace=True argument modifies the DataFrame directly.
df_combined.sort_values(by=['Company', 'Year'], inplace=True)

# --- Debugging: Check year distribution in combined DataFrame ---
print("\nYear distribution in df_combined after sorting:")
display(df_combined['Year'].value_counts().sort_index())
# --- End Debugging ---

# Calculate Sales Growth
df_combined['Sales Growth'] = df_combined.groupby('Company', observed=False)['Sales'].pct_change(fill_method=None)
# Clean up infinite values which occur when previous year's sales were 0 or very small
df_combined['Sales Growth'] = df_combined['Sales Growth'].replace([np.inf, -np.inf], np.nan)
# If current year's sales are 0, set Sales Growth to NaN as per user's request (treating 0 sales as 'missing' growth).
df_combined.loc[df_combined['Sales'] == 0, 'Sales Growth'] = np.nan
# For the first year of each company, Sales Growth will be NaN, which is appropriate.

# 7. Export the final combined file
# Save the sorted, combined DataFrame to a new CSV file.
# 'index=False' prevents Pandas from writing the DataFrame index as a column.
# 'encoding='utf-8-sig'' handles special characters correctly.
df_combined.to_csv(out_file, index=False, encoding='utf-8-sig')

print(f"\nSuccess! Created Final Master File: {out_file}")
print(f"Total Rows: {len(df_combined)}")

# Display a quick preview of the top 20 rows to verify Company #1 has all its years stacked
print("\nPreview of the top 20 rows:")
display(df_combined.head(20))
