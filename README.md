# An Empirical Evaluation of Deep Learning Models for Enhanced and Scalable Bug Detection and Classification in Large-Scale Software Systems

**SE 8101 Research Project — Sabaragamuwa University of Sri Lanka**

| Field | Detail |
|-------|--------|
| **Student** | S. Shanthosh |
| **Index Number** | 20APSE4882 |
| **Supervisor** | Mrs. W.M.L.S. Abeythunga |
| **Degree** | BSc Honours in Software Engineering |
| **Department** | Computing and Information Systems |
| **Status** | Thesis and final defence deck complete |

---

## Overview

This project presents an empirical evaluation and comparison of machine learning and deep learning models for software bug detection and classification. The primary research contribution is **imbalance-aware training using Focal Loss and Class-Weighted Focal Loss** applied to a hybrid CNN-LSTM architecture, achieving an **84.7% improvement** in bug detection Recall over the best traditional ML baseline.

---

## Key Results

| Model | Recall | F1-Score | Bugs Caught |
|-------|--------|----------|-------------|
| RF (no SMOTE) | 0.202 | 0.292 | 85 / 421 |
| RF + SMOTE *(best baseline)* | 0.451 | 0.427 | 190 / 421 |
| CNN-LSTM (BCE) | 0.577 | 0.400 | 243 / 421 |
| CNN-LSTM (Focal Loss) | 0.755 | 0.398 | 318 / 421 |
| **CNN-LSTM (Class-Weighted FL)** | **0.834** | **0.374** | **351 / 421** |
| DistilBERT (bug reports) | 1.000 | 1.000 | 120 / 120 |

---

## Project Structure

```
Research 2026/
│
├── data/
│   ├── raw/
│   │   ├── jm1.csv                  # JM1 dataset (PROMISE repository)
│   │   └── bug_reports.csv          # Synthetic bug report dataset (1,200 samples)
│   ├── processed/
│   │   └── jm1_labeled.csv          # JM1 with binary defect label (0/1)
│   └── splits/
│       ├── X_train.csv              # Training features (raw, 8,708 samples)
│       ├── y_train.csv              # Training labels (raw)
│       ├── X_train_smote.csv        # Training features (SMOTE, 14,046 samples)
│       ├── y_train_smote.csv        # Training labels (SMOTE, balanced)
│       ├── X_test.csv               # Test features (2,177 samples)
│       └── y_test.csv               # Test labels (421 defective)
│
├── notebooks/
│   ├── 01_eda.py                    # Exploratory Data Analysis
│   ├── 02_preprocessing.py          # Preprocessing pipeline (SMOTE, scaling)
│   ├── 03_baseline_models.py        # Random Forest & Naive Bayes baselines
│   ├── 04_cnn_lstm.py               # CNN-LSTM with BCE & Focal Loss
│   ├── 05_bert.py                   # DistilBERT bug report classifier
│   └── 06_final_enhancement.py      # Class-Weighted Focal Loss + 10-fold CV
│
├── models/
│   ├── cnn_lstm_bce.pth             # CNN-LSTM trained with BCE loss
│   ├── cnn_lstm_focal.pth           # CNN-LSTM trained with Focal Loss
│   ├── cnn_lstm_enhanced.pth        # CNN-LSTM trained with Class-Weighted FL
│   └── distilbert_bug_reports/      # Fine-tuned DistilBERT model
│       ├── config.json
│       ├── model.safetensors
│       ├── tokenizer.json
│       └── tokenizer_config.json
│
├── results/
│   ├── 01_class_distribution.png    # Class imbalance chart
│   ├── 02_feature_distributions.png # Feature distributions (buggy vs clean)
│   ├── 03_feature_importance_ratio.png
│   ├── 04_correlation_heatmap.png
│   ├── 05_smote_effect.png          # Before/after SMOTE
│   ├── 06–09_confusion_matrices.png # Confusion matrices (RF, NB variants)
│   ├── 10_feature_importance.png    # RF feature importance
│   ├── 11_baseline_comparison.png   # Baseline model comparison
│   ├── 12–15_cnn_lstm_charts.png    # CNN-LSTM training curves & comparison
│   ├── 16_bert_loss_curve.png       # DistilBERT training loss
│   ├── 17_bert_confusion.png        # DistilBERT confusion matrix
│   ├── 18_roc_curves.png            # ROC curves for all models
│   ├── 19_final_comparison_bar.png  # Final bar chart comparison
│   ├── 20_improvement_over_baseline.png
│   ├── 21_bugs_caught.png           # Bugs caught per model (key figure)
│   ├── baseline_results.csv         # Baseline metrics
│   ├── all_results_so_far.csv       # Incremental results
│   └── FINAL_results_table.csv      # Complete final results
│
├── Thesis/                          # FINAL THESIS (submitted deliverable)
│   ├── thesis.tex                   # LaTeX source, 5 chapters + appendices A–D
│   ├── thesis.pdf                   # Compiled thesis (79 pages)
│   ├── figures/                     # Chart PNGs referenced by the thesis
│   └── Thesis_Preparation_And_Submission_Guidelines-V1 (1).pdf
│
├── Presentation/                    # FINAL DEFENCE DECK (submitted deliverable)
│   ├── 20APSE4882.pptx              # Final defence presentation (17 slides)
│   ├── generate_presentation.py     # Deck generator (python-pptx)
│   ├── logo.jpg                     # Faculty logo extracted from the template
│   ├── FINAL Defense PPT Template_18-19(1).pptx   # Departmental template
│   └── Research Project Final Defence - Guidelines--1.pdf
│
├── report/                          # Interim deliverable (May 2026)
│   ├── Progress_Report_27May2026.pdf
│   ├── progress_report.tex          # LaTeX source for Overleaf
│   ├── generate_pdf.py              # Progress report generator
│   └── fix_chars.py                 # ASCII-safety helper for generate_pdf.py
│
├── download_dataset.py              # Downloads JM1 from OpenML
├── README.md                        # This file
└── .gitignore                       # Git ignore rules
```

---

## Setup & Installation

### Requirements

- Python 3.10+
- Windows / Linux / macOS

### Install Dependencies

```bash
pip install numpy pandas matplotlib seaborn scikit-learn imbalanced-learn
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers datasets
pip install fpdf2 python-pptx
pip install openml
```

### Run the Full Pipeline

```bash
# Step 1 — Download dataset
python download_dataset.py

# Step 2 — Exploratory Data Analysis
python notebooks/01_eda.py

# Step 3 — Preprocessing
python notebooks/02_preprocessing.py

# Step 4 — Baseline ML models
python notebooks/03_baseline_models.py

# Step 5 — CNN-LSTM (BCE + Focal Loss)
python notebooks/04_cnn_lstm.py

# Step 6 — DistilBERT bug report classifier
python notebooks/05_bert.py

# Step 7 — Enhanced CNN-LSTM + Cross-Validation
python notebooks/06_final_enhancement.py

# Step 8 — Generate the final defence presentation
python Presentation/generate_presentation.py
```

### Build the Thesis

The thesis is compiled with pdfLaTeX. Run three passes so the table of
contents, list of figures, list of tables and cross-references resolve:

```bash
cd Thesis
pdflatex thesis.tex
pdflatex thesis.tex
pdflatex thesis.tex
```

Figures resolve from `Thesis/figures/`, with `../results/` as a fallback,
so the same source compiles locally or on Overleaf.

---

## Dataset

**JM1** — NASA PROMISE Software Engineering Repository

| Property | Value |
|----------|-------|
| Source | [OpenML JM1](https://www.openml.org/d/1053) |
| Modules | 10,885 C modules |
| Features | 21 software complexity metrics |
| Target | `defects` (binary: 1=buggy, 0=clean) |
| Defective | 2,106 (19.3%) |
| Imbalance Ratio | 4.2 : 1 |

Features include Halstead complexity metrics (volume, difficulty, effort, time), McCabe cyclomatic complexity (v(g)), lines of code, operator/operand counts, and branch counts.

---

## Methodology

### Preprocessing Pipeline
1. **Median Imputation** — 25 missing values across 5 columns
2. **Winsorization** — Outlier capping at 99th percentile
3. **Stratified Split** — 80% train / 20% test (seed=42)
4. **Min-Max Normalisation** — Fitted on training set only (no leakage)
5. **BorderlineSMOTE** — Applied to training set only → 14,046 balanced samples

### Models
| Model | Type | Imbalance Strategy |
|-------|------|-------------------|
| Random Forest | Traditional ML | BorderlineSMOTE |
| Naive Bayes | Traditional ML | BorderlineSMOTE |
| CNN-LSTM (BCE) | Deep Learning | None |
| CNN-LSTM (Focal Loss) | Deep Learning | Algorithm-level (alpha=0.75, gamma=2.0) |
| CNN-LSTM (Class-Weighted FL) | Deep Learning | Algorithm-level + pos_weight=4.2 |
| DistilBERT | Transformer NLP | Balanced dataset |

### CNN-LSTM Architecture
```
Input (batch, 21, 1)
  → Conv1D(64, kernel=3) → BatchNorm
  → Conv1D(128, kernel=3) → BatchNorm
  → LSTM(hidden=64)
  → Dropout(0.4)
  → Dense(32, ReLU)
  → Output(1, Sigmoid)
Total parameters: 77,121
```

### Focal Loss (Primary Contribution)
```
FL(pt) = -alpha * (1 - pt)^gamma * log(pt)
alpha = 0.75,  gamma = 2.0

Class-Weighted FL:
loss = pos_weight * FL(pt),  pos_weight = 4.2
```

---

## Research Questions

- **RQ1** — How effectively do traditional ML models predict defects vs deep learning?
- **RQ2** — How do CNN-LSTM and BERT improve detection on imbalanced data?
- **RQ3** — What is the impact of class imbalance on model performance?
- **RQ4** — Which model achieves the best Recall / F1 balance for scalable defect detection?

---

## Outputs

| File | Description |
|------|-------------|
| `Thesis/thesis.pdf` | **Final thesis** — 79 pages, 5 chapters + appendices A–D |
| `Thesis/thesis.tex` | Thesis LaTeX source |
| `Presentation/20APSE4882.pptx` | **Final defence deck** — 17 slides |
| `report/Progress_Report_27May2026.pdf` | Interim progress report (May 2026) |
| `results/FINAL_results_table.csv` | All model metrics in one CSV |
| `models/cnn_lstm_enhanced.pth` | Best CNN-LSTM model weights |
| `models/distilbert_bug_reports/` | Fine-tuned DistilBERT model |

Both final deliverables are built to their departmental specifications:
the thesis follows *Thesis Preparation and Submission Guidelines v1.0*
(1.5in binding margin, Times New Roman, chapter/section heading styles,
IEEE references, 50-page minimum), and the deck is built on the
*FINAL Defense PPT Template* so it inherits the faculty theme, colours
and branding.

---

## License

This project is submitted for academic purposes as part of the SE 8101 Research Project module at Sabaragamuwa University of Sri Lanka. All code is original work by S. Shanthosh (20APSE4882).
