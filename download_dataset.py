"""
Step 1: Download JM1 Dataset from OpenML
JM1 is from the PROMISE repository - a NASA software defect dataset
It contains software metrics and a defect label (yes/no)
"""

print("=" * 50)
print("Downloading JM1 Dataset...")
print("=" * 50)

# Fix encoding for Windows terminal
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from sklearn.datasets import fetch_openml
import pandas as pd

# Download JM1 dataset automatically from OpenML
jm1 = fetch_openml(name='jm1', version=1, as_frame=True)
df = jm1.frame

print("\n[OK] Download complete!")
print(f"\nDataset shape: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"\nColumn names:\n{list(df.columns)}")

print(f"\nClass distribution (buggy vs not buggy):")
target_col = 'defects'
print(df[target_col].value_counts())

buggy = (df[target_col] == 'true').sum()
total = len(df)
print(f"\n   Buggy:     {buggy} ({buggy/total*100:.1f}%)")
print(f"   Not Buggy: {total-buggy} ({(total-buggy)/total*100:.1f}%)")
print(f"\n[!] This shows the CLASS IMBALANCE problem your research addresses!")

# Save to file
save_path = r'd:\Betterhalf\Research 2026\data\raw\jm1.csv'
df.to_csv(save_path, index=False)
print(f"\nSaved to: {save_path}")
print("\n[DONE] Action 3 Complete! Dataset ready.")
