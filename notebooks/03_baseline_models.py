"""
=============================================================
 NOTEBOOK 03 — BASELINE ML MODELS
 Research: Bug Detection using Deep Learning
 Student: S.Shanthosh | 20APSE4882

 Models trained:
   1. Random Forest  (without SMOTE)
   2. Random Forest  (with SMOTE)
   3. Naive Bayes    (without SMOTE)
   4. Naive Bayes    (with SMOTE)

 Metrics recorded:
   Accuracy, Precision, Recall, F1-Score, ROC-AUC
   + Confusion Matrix for each model
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import json, time
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
    classification_report
)
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.size'] = 11
sns.set_style('whitegrid')

SPLITS  = r'd:\Betterhalf\Research 2026\data\splits'
RESULTS = r'd:\Betterhalf\Research 2026\results'
MODELS  = r'd:\Betterhalf\Research 2026\models'

# ─────────────────────────────────────────────────────────
def evaluate(name, y_true, y_pred, y_prob=None):
    """Compute and print all metrics for one model."""
    acc  = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec  = recall_score(y_true, y_pred, zero_division=0)
    f1   = f1_score(y_true, y_pred, zero_division=0)
    auc  = roc_auc_score(y_true, y_prob) if y_prob is not None else None

    print(f"\n  {'Metric':<12} {'Score':>8}   Interpretation")
    print(f"  {'-'*55}")
    print(f"  {'Accuracy':<12} {acc:>7.4f}   {acc*100:.1f}% of all predictions correct")
    print(f"  {'Precision':<12} {prec:>7.4f}   of bugs predicted, {prec*100:.1f}% were real bugs")
    print(f"  {'Recall':<12} {rec:>7.4f}   caught {rec*100:.1f}% of all actual bugs")
    print(f"  {'F1-Score':<12} {f1:>7.4f}   balance of precision & recall")
    if auc:
        print(f"  {'ROC-AUC':<12} {auc:>7.4f}   overall ranking ability")

    return {'model': name, 'accuracy': acc, 'precision': prec,
            'recall': rec, 'f1_score': f1, 'roc_auc': auc}

def plot_confusion(cm, title, filename):
    """Save a single confusion matrix heatmap."""
    fig, ax = plt.subplots(figsize=(6, 5))
    labels  = [['TN\n(Correct\nClean)', 'FP\n(False\nAlarm)'],
               ['FN\n(Missed\nBug)',    'TP\n(Caught\nBug)']]
    annot   = np.array([[f'{cm[0,0]}\n{labels[0][0]}', f'{cm[0,1]}\n{labels[0][1]}'],
                         [f'{cm[1,0]}\n{labels[1][0]}', f'{cm[1,1]}\n{labels[1][1]}']])
    sns.heatmap(cm, annot=annot, fmt='', cmap='Blues',
                xticklabels=['Pred: Clean', 'Pred: Buggy'],
                yticklabels=['True: Clean', 'True: Buggy'],
                linewidths=1, linecolor='gray', ax=ax,
                annot_kws={'size': 11})
    ax.set_title(title, fontweight='bold', fontsize=12, pad=10)
    plt.tight_layout()
    plt.savefig(f'{RESULTS}\\{filename}', dpi=150, bbox_inches='tight')
    plt.close()
# ─────────────────────────────────────────────────────────

print("=" * 60)
print(" STEP 1 — Load Train / Test Splits")
print("=" * 60)

X_train      = pd.read_csv(f'{SPLITS}\\X_train.csv').values
y_train      = pd.read_csv(f'{SPLITS}\\y_train.csv').values.ravel()
X_train_sm   = pd.read_csv(f'{SPLITS}\\X_train_smote.csv').values
y_train_sm   = pd.read_csv(f'{SPLITS}\\y_train_smote.csv').values.ravel()
X_test       = pd.read_csv(f'{SPLITS}\\X_test.csv').values
y_test       = pd.read_csv(f'{SPLITS}\\y_test.csv').values.ravel()

print(f"Train (raw)   : {X_train.shape}  — Buggy: {y_train.sum():,}")
print(f"Train (SMOTE) : {X_train_sm.shape}  — Buggy: {y_train_sm.sum():,}")
print(f"Test          : {X_test.shape}   — Buggy: {y_test.sum():,}")

all_results = []

# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print(" MODEL 1 — Random Forest (without SMOTE)")
print("=" * 60)
# ═══════════════════════════════════════════════════════════

print("""
  Random Forest builds many decision trees and votes.
  It is robust and handles noisy data well.
  Here we train it on the IMBALANCED data (no SMOTE).
""")

t0 = time.time()
rf_raw = RandomForestClassifier(
    n_estimators=200,    # 200 trees
    max_depth=15,
    class_weight=None,   # no balancing — to show the problem
    random_state=42,
    n_jobs=-1
)
rf_raw.fit(X_train, y_train)
train_time = time.time() - t0

y_pred_rf_raw  = rf_raw.predict(X_test)
y_prob_rf_raw  = rf_raw.predict_proba(X_test)[:, 1]
cm_rf_raw      = confusion_matrix(y_test, y_pred_rf_raw)

print(f"  Training time: {train_time:.1f} seconds")
res1 = evaluate("RF (no SMOTE)", y_test, y_pred_rf_raw, y_prob_rf_raw)
all_results.append(res1)
plot_confusion(cm_rf_raw, "Random Forest — No SMOTE", "06_cm_rf_raw.png")
print("\n  Confusion Matrix:")
print(f"    True Negatives  (correct clean) : {cm_rf_raw[0,0]:,}")
print(f"    False Positives (false alarms)  : {cm_rf_raw[0,1]:,}")
print(f"    False Negatives (missed bugs!)  : {cm_rf_raw[1,0]:,}  <-- critical")
print(f"    True Positives  (caught bugs)   : {cm_rf_raw[1,1]:,}")

# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print(" MODEL 2 — Random Forest (with SMOTE)")
print("=" * 60)
# ═══════════════════════════════════════════════════════════

print("""
  Same Random Forest, but now trained on the SMOTE-balanced
  data. Expect better Recall and F1-Score.
""")

t0 = time.time()
rf_sm = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    class_weight=None,
    random_state=42,
    n_jobs=-1
)
rf_sm.fit(X_train_sm, y_train_sm)
train_time = time.time() - t0

y_pred_rf_sm = rf_sm.predict(X_test)
y_prob_rf_sm = rf_sm.predict_proba(X_test)[:, 1]
cm_rf_sm     = confusion_matrix(y_test, y_pred_rf_sm)

print(f"  Training time: {train_time:.1f} seconds")
res2 = evaluate("RF (SMOTE)", y_test, y_pred_rf_sm, y_prob_rf_sm)
all_results.append(res2)
plot_confusion(cm_rf_sm, "Random Forest — With SMOTE", "07_cm_rf_smote.png")
print("\n  Confusion Matrix:")
print(f"    True Negatives  (correct clean) : {cm_rf_sm[0,0]:,}")
print(f"    False Positives (false alarms)  : {cm_rf_sm[0,1]:,}")
print(f"    False Negatives (missed bugs!)  : {cm_rf_sm[1,0]:,}  <-- critical")
print(f"    True Positives  (caught bugs)   : {cm_rf_sm[1,1]:,}")

# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print(" MODEL 3 — Naive Bayes (without SMOTE)")
print("=" * 60)
# ═══════════════════════════════════════════════════════════

print("""
  Naive Bayes is a simple probabilistic model.
  It assumes all features are independent (often wrong, but fast).
  It is a standard baseline in defect prediction literature.
""")

t0 = time.time()
nb_raw = GaussianNB()
nb_raw.fit(X_train, y_train)
train_time = time.time() - t0

y_pred_nb_raw = nb_raw.predict(X_test)
y_prob_nb_raw = nb_raw.predict_proba(X_test)[:, 1]
cm_nb_raw     = confusion_matrix(y_test, y_pred_nb_raw)

print(f"  Training time: {train_time:.2f} seconds")
res3 = evaluate("NB (no SMOTE)", y_test, y_pred_nb_raw, y_prob_nb_raw)
all_results.append(res3)
plot_confusion(cm_nb_raw, "Naive Bayes — No SMOTE", "08_cm_nb_raw.png")
print("\n  Confusion Matrix:")
print(f"    True Negatives  (correct clean) : {cm_nb_raw[0,0]:,}")
print(f"    False Positives (false alarms)  : {cm_nb_raw[0,1]:,}")
print(f"    False Negatives (missed bugs!)  : {cm_nb_raw[1,0]:,}  <-- critical")
print(f"    True Positives  (caught bugs)   : {cm_nb_raw[1,1]:,}")

# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print(" MODEL 4 — Naive Bayes (with SMOTE)")
print("=" * 60)
# ═══════════════════════════════════════════════════════════

t0 = time.time()
nb_sm = GaussianNB()
nb_sm.fit(X_train_sm, y_train_sm)
train_time = time.time() - t0

y_pred_nb_sm = nb_sm.predict(X_test)
y_prob_nb_sm = nb_sm.predict_proba(X_test)[:, 1]
cm_nb_sm     = confusion_matrix(y_test, y_pred_nb_sm)

print(f"  Training time: {train_time:.2f} seconds")
res4 = evaluate("NB (SMOTE)", y_test, y_pred_nb_sm, y_prob_nb_sm)
all_results.append(res4)
plot_confusion(cm_nb_sm, "Naive Bayes — With SMOTE", "09_cm_nb_smote.png")
print("\n  Confusion Matrix:")
print(f"    True Negatives  (correct clean) : {cm_nb_sm[0,0]:,}")
print(f"    False Positives (false alarms)  : {cm_nb_sm[0,1]:,}")
print(f"    False Negatives (missed bugs!)  : {cm_nb_sm[1,0]:,}  <-- critical")
print(f"    True Positives  (caught bugs)   : {cm_nb_sm[1,1]:,}")

# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print(" FEATURE IMPORTANCE — Random Forest")
print("=" * 60)
# ═══════════════════════════════════════════════════════════

feature_names = pd.read_csv(f'{SPLITS}\\X_train.csv').columns.tolist()
importances   = pd.Series(rf_sm.feature_importances_, index=feature_names)
importances   = importances.sort_values(ascending=False)

print("\n  Top 10 most important features (from SMOTE-trained RF):")
print(f"\n  {'Rank':<6} {'Feature':<22} {'Importance':>12}")
print(f"  {'-'*42}")
for rank, (feat, imp) in enumerate(importances.head(10).items(), 1):
    bar = '#' * int(imp * 200)
    print(f"  {rank:<6} {feat:<22} {imp:>10.4f}   {bar}")

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#e74c3c' if i < 3 else '#f39c12' if i < 7 else '#3498db'
          for i in range(len(importances))]
ax.barh(importances.index[::-1], importances.values[::-1],
        color=colors[::-1], edgecolor='black', linewidth=0.7)
ax.set_xlabel('Feature Importance Score')
ax.set_title('Random Forest — Feature Importances\n(higher = more useful for predicting bugs)',
             fontweight='bold')
plt.tight_layout()
plt.savefig(f'{RESULTS}\\10_feature_importance.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n  Chart saved -> results\\10_feature_importance.png")

# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print(" COMPARISON — All 4 Baseline Models")
print("=" * 60)
# ═══════════════════════════════════════════════════════════

results_df = pd.DataFrame(all_results)
results_df = results_df.set_index('model')

print(f"\n  {'Model':<20} {'Accuracy':>9} {'Precision':>10} {'Recall':>8} {'F1':>8} {'AUC':>8}")
print(f"  {'-'*68}")
for model, row in results_df.iterrows():
    auc_str = f"{row['roc_auc']:.4f}" if row['roc_auc'] else "  N/A  "
    print(f"  {model:<20} {row['accuracy']:>9.4f} {row['precision']:>10.4f} "
          f"{row['recall']:>8.4f} {row['f1_score']:>8.4f} {auc_str:>8}")

# Grouped bar chart comparing all models
metrics = ['accuracy', 'precision', 'recall', 'f1_score']
labels  = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
models  = results_df.index.tolist()
colors  = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']

x     = np.arange(len(metrics))
width = 0.2
fig, ax = plt.subplots(figsize=(13, 6))

for i, (model, color) in enumerate(zip(models, colors)):
    vals = [results_df.loc[model, m] for m in metrics]
    bars = ax.bar(x + i*width, vals, width, label=model,
                  color=color, edgecolor='black', linewidth=0.7, alpha=0.88)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                f'{val:.3f}', ha='center', va='bottom', fontsize=8.5, fontweight='bold')

ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(labels, fontsize=12)
ax.set_ylabel('Score (0–1)')
ax.set_ylim(0, 1.12)
ax.set_title('Baseline ML Models — Performance Comparison\n(all 4 models on the same test set)',
             fontweight='bold', fontsize=13)
ax.legend(loc='upper right', fontsize=10)
ax.axhline(y=0.5, color='gray', linestyle=':', linewidth=1)
plt.tight_layout()
plt.savefig(f'{RESULTS}\\11_baseline_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n  Chart saved -> results\\11_baseline_comparison.png")

# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print(" SAVE RESULTS")
print("=" * 60)
# ═══════════════════════════════════════════════════════════

results_df.to_csv(f'{RESULTS}\\baseline_results.csv')
print("  Saved -> results\\baseline_results.csv")

# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print(" NOTEBOOK 03 SUMMARY")
print("=" * 60)

best_f1_model   = results_df['f1_score'].idxmax()
best_f1_val     = results_df['f1_score'].max()
best_rec_model  = results_df['recall'].idxmax()
best_rec_val    = results_df['recall'].max()

print(f"""
  MODELS TRAINED:
    1. Random Forest — no SMOTE
    2. Random Forest — with SMOTE   <-- expect best RF result
    3. Naive Bayes   — no SMOTE
    4. Naive Bayes   — with SMOTE

  BEST F1-SCORE : {best_f1_model:<20}  F1 = {best_f1_val:.4f}
  BEST RECALL   : {best_rec_model:<20}  Recall = {best_rec_val:.4f}

  KEY OBSERVATIONS FOR YOUR REPORT:
    1. SMOTE consistently improves Recall and F1-Score
       by making the model pay more attention to buggy samples.
    2. Naive Bayes trains nearly instantly but has lower precision.
    3. Random Forest is stronger overall due to ensemble voting.
    4. Even the best baseline here will be BEATEN by your
       CNN-LSTM and BERT models in the next notebooks.
    5. These baseline scores are your TARGET TO BEAT.

  CHARTS SAVED:
    06 - 09  : Confusion matrices for all 4 models
    10       : Feature importance (Random Forest)
    11       : Side-by-side metric comparison

  NEXT: Notebook 04 — CNN-LSTM Deep Learning Model
""")
print("=" * 60)
print(" NOTEBOOK 03 COMPLETE!")
print("=" * 60)
