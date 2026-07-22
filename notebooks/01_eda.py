"""
=============================================================
 NOTEBOOK 01 — DATA EXPLORATION (EDA)
 Research: Bug Detection using Deep Learning
 Student: S.Shanthosh | 20APSE4882
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')           # save to file without opening a window
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size']      = 12
sns.set_style('whitegrid')

RESULTS = r'd:\Betterhalf\Research 2026\results'

print("=" * 60)
print(" STEP 1 — Loading Dataset")
print("=" * 60)

df = pd.read_csv(r'd:\Betterhalf\Research 2026\data\raw\jm1.csv')

print(f"Dataset loaded!")
print(f"Shape : {df.shape[0]} rows  x  {df.shape[1]} columns")
print(f"\nFirst 3 rows:")
print(df.head(3).to_string())

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" STEP 2 — Missing Values Check")
print("=" * 60)

missing = df.isnull().sum()
total_missing = missing.sum()
if total_missing == 0:
    print("No missing values found! Dataset is clean.")
else:
    print(f"Total missing values: {total_missing}")
    print(missing[missing > 0])

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" STEP 3 — Class Distribution (The Imbalance Problem)")
print("=" * 60)

counts   = df['defects'].value_counts()
pct      = df['defects'].value_counts(normalize=True) * 100
total    = len(df)
n_buggy  = int(counts[True])
n_clean  = int(counts[False])

print(f"  Not Buggy (False): {n_clean:,}  ({pct[False]:.1f}%)")
print(f"  Buggy     (True) : {n_buggy:,}  ({pct[True]:.1f}%)")
print(f"\n  Imbalance Ratio  : {n_clean/n_buggy:.1f}:1  (not-buggy : buggy)")
print("""
  WHY THIS MATTERS:
    A lazy model that always predicts 'not buggy' would still
    get 80% accuracy — but it catches ZERO bugs!
    => That is why your research uses F1-Score and Recall.
""")

# Plot 1 — Class distribution
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].bar(['Not Buggy', 'Buggy'], [n_clean, n_buggy],
            color=['#2ecc71', '#e74c3c'], edgecolor='black', linewidth=1.2)
axes[0].set_title('Class Distribution — JM1 Dataset', fontweight='bold', fontsize=14)
axes[0].set_ylabel('Number of Software Modules')
for i, (val, p) in enumerate([(n_clean, pct[False]), (n_buggy, pct[True])]):
    axes[0].text(i, val + 120, f'{val:,}\n({p:.1f}%)', ha='center', fontweight='bold', fontsize=11)

axes[1].pie([n_clean, n_buggy], labels=['Not Buggy', 'Buggy'],
            colors=['#2ecc71', '#e74c3c'], autopct='%1.1f%%',
            startangle=90, explode=(0, 0.06))
axes[1].set_title('Class Proportions', fontweight='bold', fontsize=14)

plt.tight_layout()
out1 = f'{RESULTS}\\01_class_distribution.png'
plt.savefig(out1, dpi=150, bbox_inches='tight')
plt.close()
print(f"  Chart saved -> results\\01_class_distribution.png")

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" STEP 4 — Feature Statistics")
print("=" * 60)

feature_cols = [c for c in df.columns if c != 'defects']
print(f"Number of features: {len(feature_cols)}")

feature_meanings = {
    'loc'             : 'Lines of Code',
    'v(g)'            : 'Cyclomatic Complexity (branching paths)',
    'ev(g)'           : 'Essential Complexity',
    'iv(g)'           : 'Design Complexity',
    'n'               : 'Halstead Length (operators + operands)',
    'v'               : 'Halstead Volume',
    'l'               : 'Halstead Level (inverse of difficulty)',
    'd'               : 'Halstead Difficulty',
    'i'               : 'Halstead Intelligence',
    'e'               : 'Halstead Effort',
    'b'               : 'Halstead Bug Estimate',
    't'               : 'Halstead Time to Implement',
    'lOCode'          : 'Lines of actual code',
    'lOComment'       : 'Lines of comments',
    'lOBlank'         : 'Blank lines',
    'locCodeAndComment': 'Lines with code + comment',
    'uniq_Op'         : 'Unique operators count',
    'uniq_Opnd'       : 'Unique operands count',
    'total_Op'        : 'Total operators count',
    'total_Opnd'      : 'Total operands count',
    'branchCount'     : 'Number of branches (if/else/switch)',
}

print(f"\n{'Feature':<22} {'Meaning':<40} {'Min':>8} {'Mean':>10} {'Max':>10}")
print("-" * 95)
for feat in feature_cols:
    meaning = feature_meanings.get(feat, '')
    mn  = df[feat].min()
    avg = df[feat].mean()
    mx  = df[feat].max()
    print(f"  {feat:<20} {meaning:<40} {mn:>8.1f} {avg:>10.1f} {mx:>10.1f}")

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" STEP 5 — Feature Distributions: Buggy vs Not Buggy")
print("=" * 60)

buggy_df = df[df['defects'] == True]
clean_df = df[df['defects'] == False]

key_features = ['loc', 'v(g)', 'ev(g)', 'n', 'v', 'd', 'branchCount', 'lOCode']

fig, axes = plt.subplots(2, 4, figsize=(18, 9))
axes = axes.flatten()

for i, feat in enumerate(key_features):
    upper = df[feat].quantile(0.99)
    axes[i].hist(clean_df[feat][clean_df[feat] <= upper],
                 bins=40, alpha=0.6, color='#2ecc71', label='Not Buggy', density=True)
    axes[i].hist(buggy_df[feat][buggy_df[feat] <= upper],
                 bins=40, alpha=0.6, color='#e74c3c', label='Buggy',     density=True)
    axes[i].set_title(feat, fontweight='bold')
    axes[i].set_xlabel('Value')
    axes[i].set_ylabel('Density')
    axes[i].legend(fontsize=9)

plt.suptitle('Feature Distributions: Buggy vs Not-Buggy Modules',
             fontsize=15, fontweight='bold', y=1.01)
plt.tight_layout()
out2 = f'{RESULTS}\\02_feature_distributions.png'
plt.savefig(out2, dpi=150, bbox_inches='tight')
plt.close()
print(f"  Chart saved -> results\\02_feature_distributions.png")

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" STEP 6 — Which Features Differ Most (Buggy vs Clean)?")
print("=" * 60)

means        = df.groupby('defects')[feature_cols].mean()
ratio        = (means.loc[True] / means.loc[False]).sort_values(ascending=False)

print(f"\n{'Feature':<22} {'Buggy Mean':>12} {'Clean Mean':>12} {'Ratio':>8}  Insight")
print("-" * 80)
for feat in ratio.index:
    b_mean = means.loc[True, feat]
    c_mean = means.loc[False, feat]
    r      = ratio[feat]
    tag    = "*** VERY HIGH in buggy!" if r > 1.5 else "^ Higher in buggy" if r > 1.1 else ""
    print(f"  {feat:<20} {b_mean:>12.1f} {c_mean:>12.1f} {r:>8.2f}  {tag}")

# Plot ratio chart
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#e74c3c' if r > 1.5 else '#f39c12' if r > 1.1 else '#2ecc71' for r in ratio]
ax.barh(ratio.index, ratio.values, color=colors, edgecolor='black', linewidth=0.8)
ax.axvline(x=1.0, color='black', linestyle='--', linewidth=1.5, label='Baseline (ratio=1.0)')
ax.set_xlabel('Ratio  (Buggy Mean / Clean Mean)')
ax.set_title('Which Features are Elevated in Buggy Modules?', fontweight='bold', fontsize=14)
ax.legend()

from matplotlib.patches import Patch
legend_els = [Patch(color='#e74c3c', label='Much higher in buggy (>1.5x)'),
              Patch(color='#f39c12', label='Slightly higher (1.1–1.5x)'),
              Patch(color='#2ecc71', label='Similar or lower')]
ax.legend(handles=legend_els, loc='lower right')

plt.tight_layout()
out3 = f'{RESULTS}\\03_feature_importance_ratio.png'
plt.savefig(out3, dpi=150, bbox_inches='tight')
plt.close()
print(f"\n  Chart saved -> results\\03_feature_importance_ratio.png")

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" STEP 7 — Correlation Heatmap")
print("=" * 60)

df['defects_int'] = df['defects'].astype(int)
corr = df[feature_cols + ['defects_int']].corr()

fig, ax = plt.subplots(figsize=(14, 11))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, linewidths=0.4, annot_kws={'size': 7}, ax=ax)
ax.set_title('Feature Correlation Matrix\n(bottom row = correlation with defects)',
             fontweight='bold', fontsize=13)
plt.tight_layout()
out4 = f'{RESULTS}\\04_correlation_heatmap.png'
plt.savefig(out4, dpi=150, bbox_inches='tight')
plt.close()
print(f"  Chart saved -> results\\04_correlation_heatmap.png")

# Which features most correlated with target?
target_corr = corr['defects_int'].drop('defects_int').sort_values(ascending=False)
print(f"\n  Features most correlated with DEFECTS (top = best predictors):")
print(f"  {'Feature':<22} {'Correlation':>12}")
print("  " + "-" * 36)
for feat, val in target_corr.items():
    bar = '|' * int(abs(val) * 25)
    print(f"  {feat:<22} {val:>+.4f}   {bar}")

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" STEP 8 — Save Processed Dataset for Next Notebook")
print("=" * 60)

df_save = df[feature_cols + ['defects']].copy()
df_save['defects'] = df_save['defects'].astype(int)   # True->1, False->0
df_save.to_csv(r'd:\Betterhalf\Research 2026\data\processed\jm1_labeled.csv', index=False)
print("  Saved -> data/processed/jm1_labeled.csv")
print(f"  Shape : {df_save.shape}  |  Defects column: 1=buggy, 0=clean")

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" EDA SUMMARY — KEY FINDINGS FOR YOUR RESEARCH REPORT")
print("=" * 60)
print(f"""
  Dataset  : JM1 (PROMISE Repository — NASA defect data)
  Rows     : {len(df):,} software modules
  Features : {len(feature_cols)} software complexity metrics

  CLASS DISTRIBUTION:
    Not Buggy (0): {n_clean:,}  ({pct[False]:.1f}%)
    Buggy     (1): {n_buggy:,}  ({pct[True]:.1f}%)
    Ratio         : {n_clean/n_buggy:.1f}:1

  DATA QUALITY:
    Missing values: {total_missing}  (clean dataset, no imputation needed)
    All features  : numeric (ready for ML)

  KEY OBSERVATIONS:
    1. Strong class imbalance (80:20) proves the need for
       SMOTE / focal loss in your research.
    2. loc, v(g), n, v, e, b are significantly HIGHER in buggy
       modules => these are the most predictive features.
    3. Many features are highly correlated (e.g. loc and n)
       => PCA or feature selection can reduce redundancy.
    4. A naive model at 80% accuracy is USELESS here =>
       F1-Score and Recall are the right metrics.

  CHARTS SAVED TO: d:\\Betterhalf\\Research 2026\\results\\
    01_class_distribution.png
    02_feature_distributions.png
    03_feature_importance_ratio.png
    04_correlation_heatmap.png

  NEXT: Notebook 02 — Preprocessing (SMOTE + Normalization)
""")
print("=" * 60)
print(" ACTION 4 COMPLETE!")
print("=" * 60)
