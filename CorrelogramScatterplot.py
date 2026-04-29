import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Define the base path for Google Drive
base_path = '/content/drive/MyDrive/Github-Cursor/Shariah Compliance Project/'

# Load the clean dataset using the full path
df = pd.read_csv(base_path + "final_unbalanced_panel_2026.csv")
cols = ['ROA', 'DR', 'IR', 'IncR', 'NLA', 'IAR']

# Drop missing values specifically for this plot to ensure consistency
df_plot = df[cols].dropna()

# Set professional aesthetics
sns.set_theme(style="white", palette="muted")
plt.rcParams.update({'font.size': 16, 'font.family': 'serif'})

# Initialize the PairGrid
g = sns.PairGrid(df_plot, diag_sharey=False)

# 1. Map the Lower Triangle: Scatter plots with regression lines
g.map_lower(sns.regplot, scatter_kws={'alpha':0.2, 's':10}, line_kws={'color':'red', 'lw':1})

# 2. Map the Diagonal: Distribution (KDE)
g.map_diag(sns.kdeplot, lw=2, fill=True)

# 3. Map the Upper Triangle: Correlation Coefficients as text
def corr_func(x, y, **kwargs):
    r = np.corrcoef(x, y)[0, 1]
    ax = plt.gca()
    ax.annotate(f"r = {r:.2f}", xy=(.5, .5), xycoords=ax.transAxes,
                ha='center', va='center', fontsize=12, fontweight='bold')

g.map_upper(corr_func)

# Formatting the final figure
plt.subplots_adjust(top=0.95)
g.fig.suptitle('Correlogram - Scatterplot Matrix & Correlation Coefficients',
               fontsize=16, fontweight='bold')

# Save for thesis
g.savefig(base_path + 'correlogram_matrix.png', dpi=300)
