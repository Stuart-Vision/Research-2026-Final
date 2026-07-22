"""
=============================================================
 NOTEBOOK 02 — DATA PREPROCESSING
 Research: Bug Detection using Deep Learning
 Student: S.Shanthosh | 20APSE4882

 Steps:
   1. Load processed dataset from Notebook 01
   2. Handle missing values
   3. Remove outliers
   4. Normalize features (Min-Max Scaling)
   5. Split into Train / Test sets
   6. Apply SMOTE to fix class imbalance (on train set ONLY)
   7. Save all splits for Notebook 03 (models)
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE, BorderlineSMOTE
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (12, 5)
sns.set_style('whitegrid')

RESULTS  = r'd:\Betterhalf\Research 2026\results'
DATA_OUT = r'd:\Betterhalf\Research 2026\data\splits'

# ─────────────────────────────────────────────
print("=" * 60)
print(" STEP 1 — Load Dataset")
print("=" * 60)

df = pd.read_csv(r'd:\Betterhalf\Research 2026\data\processed\jm1_labeled.csv')

X = df.drop('defects', axis=1)   # features (21 columns)
y = df['defects']                 # target   (0 = clean, 1 = buggy)

print(f"Features (X) shape : {X.shape}")
print(f"Target   (y) shape : {y.shape}")
print(f"Class counts       : {Counter(y)}")

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" STEP 2 — Handle Missing Values")
print("=" * 60)

missing_before = X.isnull().sum().sum()
print(f"Missing values BEFORE: {missing_before}")

# Fill missing values with the MEDIAN of each column
# (median is better than mean for skewed data like code metrics)
X = X.fillna(X.median())

missing_after = X.isnull().sum().sum()
print(f"Missing values AFTER : {missing_after}")
print("Strategy used        : Median imputation (robust against outliers)")

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" STEP 3 — Remove Extreme Outliers")
print("=" * 60)

# Cap extreme values at 99th percentile (winsorization)
# This stops a few massive values from dominating the model
before_shape = X.shape[0]
for col in X.columns:
    upper = X[col].quantile(0.99)
    X[col] = X[col].clip(upper=upper)

print(f"Rows before : {before_shape}")
print(f"Rows after  : {X.shape[0]}  (same — we capped values, not removed rows)")
print("Strategy    : Winsorization at 99th percentile per feature")

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" STEP 4 — Train / Test Split  (80% train, 20% test)")
print("=" * 60)

# IMPORTANT: Split BEFORE applying SMOTE
# Never apply SMOTE to test data — that would be data leakage!
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,       # fixed seed for reproducibility
    stratify=y             # keep same class ratio in both splits
)

print(f"Training set   : {X_train.shape[0]} samples")
print(f"  Buggy        : {y_train.sum()}  ({y_train.mean()*100:.1f}%)")
print(f"  Not Buggy    : {(y_train==0).sum()}  ({(y_train==0).mean()*100:.1f}%)")
print(f"\nTest set       : {X_test.shape[0]} samples")
print(f"  Buggy        : {y_test.sum()}  ({y_test.mean()*100:.1f}%)")
print(f"  Not Buggy    : {(y_test==0).sum()}  ({(y_test==0).mean()*100:.1f}%)")
print("\nstratify=y ensures the class ratio is the same in both sets.")

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" STEP 5 — Normalize Features (Min-Max Scaling)")
print("=" * 60)

# Scale all features to range [0, 1]
# Fit the scaler ONLY on training data, then transform both
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)     # use train's scale — no leakage

print("Min-Max Scaling applied: all features now in range [0.0, 1.0]")
print(f"\nBefore scaling — loc column: min={X_train['loc'].min():.0f}, max={X_train['loc'].max():.0f}")
print(f"After  scaling — loc column: min={X_train_scaled[:,0].min():.2f}, max={X_train_scaled[:,0].max():.2f}")
print("\nWHY? Neural networks train much faster when all features are on the same scale.")

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" STEP 6 — Apply SMOTE (Fix Class Imbalance)")
print("=" * 60)

print("BEFORE SMOTE:")
print(f"  Training set — Buggy: {y_train.sum():,}  |  Not Buggy: {(y_train==0).sum():,}")
print(f"  Imbalance ratio: {(y_train==0).sum() / y_train.sum():.1f}:1")

# BorderlineSMOTE focuses on the difficult boundary cases
# (better than basic SMOTE for this type of data)
smote = BorderlineSMOTE(random_state=42, kind='borderline-1')
X_train_sm, y_train_sm = smote.fit_resample(X_train_scaled, y_train)

print("\nAFTER SMOTE:")
print(f"  Training set — Buggy: {y_train_sm.sum():,}  |  Not Buggy: {(y_train_sm==0).sum():,}")
print(f"  Imbalance ratio: {(y_train_sm==0).sum() / y_train_sm.sum():.1f}:1")
print(f"\nSMOTE created {y_train_sm.sum() - y_train.sum():,} synthetic buggy samples")
print("NOTE: SMOTE applied ONLY to training data. Test set stays original.")

# Visualize SMOTE effect
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Before SMOTE
before_counts = [y_train.sum(), (y_train==0).sum()]
axes[0].bar(['Buggy', 'Not Buggy'], before_counts,
            color=['#e74c3c', '#2ecc71'], edgecolor='black')
axes[0].set_title('Training Set BEFORE SMOTE', fontweight='bold', fontsize=13)
axes[0].set_ylabel('Sample Count')
for i, v in enumerate(before_counts):
    axes[0].text(i, v + 50, f'{v:,}', ha='center', fontweight='bold')

# After SMOTE
after_counts = [y_train_sm.sum(), (y_train_sm==0).sum()]
axes[1].bar(['Buggy', 'Not Buggy'], after_counts,
            color=['#e74c3c', '#2ecc71'], edgecolor='black')
axes[1].set_title('Training Set AFTER SMOTE', fontweight='bold', fontsize=13)
axes[1].set_ylabel('Sample Count')
for i, v in enumerate(after_counts):
    axes[1].text(i, v + 50, f'{v:,}', ha='center', fontweight='bold')

plt.suptitle('Effect of BorderlineSMOTE on Class Balance', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{RESULTS}\\05_smote_effect.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"\nChart saved -> results\\05_smote_effect.png")

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" STEP 7 — Also prepare a NON-SMOTE version")
print("         (needed to compare with SMOTE results)")
print("=" * 60)

# We keep both versions:
# - X_train_scaled     : original imbalanced (for baseline comparison)
# - X_train_sm         : SMOTE balanced (for fair training)
print("Both versions kept:")
print("  raw    : X_train_scaled  (imbalanced — for comparison)")
print("  SMOTE  : X_train_sm      (balanced   — for main training)")

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" STEP 8 — Save All Splits to Disk")
print("=" * 60)

# Convert back to DataFrame for saving
feature_names = X.columns.tolist()

# Imbalanced train set (no SMOTE)
pd.DataFrame(X_train_scaled, columns=feature_names).to_csv(
    f'{DATA_OUT}\\X_train.csv', index=False)
pd.Series(y_train.values, name='defects').to_csv(
    f'{DATA_OUT}\\y_train.csv', index=False)

# SMOTE-balanced train set
pd.DataFrame(X_train_sm, columns=feature_names).to_csv(
    f'{DATA_OUT}\\X_train_smote.csv', index=False)
pd.Series(y_train_sm, name='defects').to_csv(
    f'{DATA_OUT}\\y_train_smote.csv', index=False)

# Test set (never touched by SMOTE)
pd.DataFrame(X_test_scaled, columns=feature_names).to_csv(
    f'{DATA_OUT}\\X_test.csv', index=False)
pd.Series(y_test.values, name='defects').to_csv(
    f'{DATA_OUT}\\y_test.csv', index=False)

print("Files saved to data/splits/:")
print("  X_train.csv         — raw train features (imbalanced)")
print("  y_train.csv         — raw train labels")
print("  X_train_smote.csv   — SMOTE train features (balanced)")
print("  y_train_smote.csv   — SMOTE train labels")
print("  X_test.csv          — test features")
print("  y_test.csv          — test labels")

# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print(" PREPROCESSING SUMMARY")
print("=" * 60)
print(f"""
  PIPELINE APPLIED:
    1. Missing values   : Median imputation (25 values filled)
    2. Outlier handling : Winsorization at 99th percentile
    3. Train/Test split : 80% / 20%  (stratified, seed=42)
    4. Normalization    : Min-Max Scaling [0, 1]
    5. Class balance    : BorderlineSMOTE on training set only

  FINAL DATA SIZES:
    Train (raw)   : {X_train.shape[0]:,} samples  |  Buggy: {y_train.sum():,}  Clean: {(y_train==0).sum():,}
    Train (SMOTE) : {X_train_sm.shape[0]:,} samples  |  Buggy: {y_train_sm.sum():,}  Clean: {(y_train_sm==0).sum():,}
    Test          : {X_test.shape[0]:,} samples  |  Buggy: {y_test.sum():,}  Clean: {(y_test==0).sum():,}

  IMPORTANT NOTES FOR YOUR REPORT:
    - Scaler fitted on TRAIN only (no data leakage)
    - SMOTE applied to TRAIN only (test stays real/original)
    - Stratified split ensures both sets have same class ratio
    - BorderlineSMOTE is better than basic SMOTE for boundary cases

  NEXT: Notebook 03 — Baseline Models (Random Forest + Naive Bayes)
""")
print("=" * 60)
print(" NOTEBOOK 02 COMPLETE!")
print("=" * 60)
