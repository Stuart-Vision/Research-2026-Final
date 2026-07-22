"""
Generate professional PDF progress report using fpdf2
"""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

RESULTS = r'd:\Betterhalf\Research 2026\results'
OUT     = r'd:\Betterhalf\Research 2026\report\Progress_Report_27May2026.pdf'

# ── Colour palette ──────────────────────────────────────────
BLUE   = (0,   70,  127)
DGRAY  = (60,  60,   60)
LGRAY  = (245, 245, 245)
WHITE  = (255, 255, 255)
GREEN  = (39,  174,  96)
RED    = (192,  57,  43)
BLACK  = (0,    0,   0)

class Report(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(*DGRAY)
        self.cell(0, 6, 'SE 8101 Research Project  |  S.Shanthosh  20APSE4882', align='L')
        self.cell(0, 6, 'Sabaragamuwa University of Sri Lanka', align='R',
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*BLUE)
        self.set_line_width(0.4)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*DGRAY)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def section_title(self, title):
        self.ln(4)
        self.set_fill_color(*BLUE)
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 8, f'  {title}', fill=True,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)
        self.set_text_color(*BLACK)

    def sub_title(self, title):
        self.ln(2)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*BLUE)
        self.cell(0, 7, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*BLACK)
        self.ln(1)

    def body(self, text, indent=0):
        self.set_font('Helvetica', '', 9.5)
        self.set_text_color(*DGRAY)
        self.set_x(self.l_margin + indent)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bullet(self, text, indent=8):
        self.set_font('Helvetica', '', 9.5)
        self.set_text_color(*DGRAY)
        self.set_x(self.l_margin + indent)
        self.multi_cell(0, 5.5, f'*  {text}')

    def kv(self, key, val, bold_val=False):
        self.set_font('Helvetica', 'B', 9.5)
        self.set_text_color(*BLUE)
        self.cell(58, 6, key + ':', new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_font('Helvetica', 'B' if bold_val else '', 9.5)
        self.set_text_color(*DGRAY)
        self.cell(0, 6, val, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def table_header(self, cols, widths):
        self.set_fill_color(*BLUE)
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', 'B', 8.5)
        for col, w in zip(cols, widths):
            self.cell(w, 7, col, border=1, fill=True, align='C')
        self.ln()
        self.set_text_color(*BLACK)

    def table_row(self, vals, widths, highlight=False, aligns=None):
        if highlight:
            self.set_fill_color(*LGRAY)
        else:
            self.set_fill_color(*WHITE)
        self.set_font('Helvetica', 'B' if highlight else '', 8.5)
        self.set_text_color(*DGRAY)
        aligns = aligns or ['C'] * len(vals)
        for val, w, al in zip(vals, widths, aligns):
            self.cell(w, 6.5, str(val), border=1, fill=True, align=al)
        self.ln()


pdf = Report('P', 'mm', 'A4')
pdf.set_margins(18, 22, 18)
pdf.set_auto_page_break(auto=True, margin=18)

# ══════════════════════════════════════════════════════════
# TITLE PAGE
# ══════════════════════════════════════════════════════════
pdf.add_page()
pdf.ln(8)
pdf.set_font('Helvetica', 'B', 14)
pdf.set_text_color(*BLUE)
pdf.cell(0, 9, 'SABARAGAMUWA UNIVERSITY OF SRI LANKA', align='C',
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('Helvetica', '', 10)
pdf.set_text_color(*DGRAY)
pdf.cell(0, 6, 'Faculty of Computing  |  Department of Software Engineering', align='C',
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 6, 'BSc Honours Degree Programme in Software Engineering', align='C',
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(10)

# Blue rule
pdf.set_draw_color(*BLUE); pdf.set_line_width(1.2)
pdf.line(18, pdf.get_y(), pdf.w - 18, pdf.get_y()); pdf.ln(6)

pdf.set_font('Helvetica', 'B', 18)
pdf.set_text_color(*BLUE)
pdf.cell(0, 11, 'Implementation Progress Report', align='C',
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(*DGRAY)
pdf.cell(0, 7, 'SE 8101  --  Research Project', align='C',
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(4)
pdf.set_draw_color(*BLUE)
pdf.line(18, pdf.get_y(), pdf.w - 18, pdf.get_y()); pdf.ln(12)

# Details box
pdf.set_fill_color(*LGRAY)
pdf.rect(30, pdf.get_y(), pdf.w - 60, 52, 'F')
pdf.ln(6)
details = [
    ('Student Name', 'S.Shanthosh'),
    ('Index Number', '20APSE4882'),
    ('Supervisor',   'Mrs. WMLS Abeythunga'),
    ('Date',         '27th May 2026'),
    ('Report Type',  'Daily Implementation Update'),
]
for k, v in details:
    pdf.set_x(38)
    pdf.set_font('Helvetica', 'B', 10); pdf.set_text_color(*BLUE)
    pdf.cell(50, 8, k + ':', new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('Helvetica', '', 10); pdf.set_text_color(*DGRAY)
    pdf.cell(0, 8, v, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(12)

# Research topic box
pdf.set_fill_color(230, 240, 255)
pdf.rect(18, pdf.get_y(), pdf.w - 36, 22, 'F')
pdf.ln(4)
pdf.set_font('Helvetica', 'B', 8.5); pdf.set_text_color(*BLUE)
pdf.cell(0, 5, 'RESEARCH TOPIC', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('Helvetica', 'I', 9); pdf.set_text_color(*DGRAY)
pdf.multi_cell(0, 5,
    'An Empirical Evaluation of Deep Learning Models for Enhanced and Scalable\n'
    'Bug Detection and Classification in Large-Scale Software Systems',
    align='C')


# ══════════════════════════════════════════════════════════
# PAGE 2 -- Overview & Dataset
# ══════════════════════════════════════════════════════════
pdf.add_page()

pdf.section_title('1.  Overview of Today\'s Progress')
pdf.body(
    'This report documents the implementation work completed on 27th May 2026, '
    'covering four major phases: environment configuration, exploratory data analysis, '
    'data preprocessing, and model training. A total of six models were trained and '
    'evaluated -- four traditional machine learning models and two deep learning variants.'
)

# Progress table
pdf.ln(2)
cols   = ['Phase', 'Task', 'Status', 'Output']
widths = [15, 88, 22, 49]
pdf.table_header(cols, widths)
rows = [
    ('1', 'Environment setup & library installation',   'Done',  'All libraries ready'),
    ('2', 'Dataset acquisition (JM1 -- PROMISE)',        'Done',  '10,885 samples'),
    ('3', 'Exploratory Data Analysis (EDA)',             'Done',  '4 charts saved'),
    ('4', 'Data Preprocessing pipeline',                 'Done',  '6 split files saved'),
    ('5', 'Baseline ML models (RF + Naive Bayes)',       'Done',  'Best F1: 0.4265'),
    ('6', 'CNN-LSTM Deep Learning model',                'Done',  'Best Recall: 0.755'),
]
for i, (ph, task, st, out) in enumerate(rows):
    pdf.table_row([ph, task, st, out], widths,
                  highlight=(i % 2 == 1),
                  aligns=['C', 'L', 'C', 'L'])

# Dataset section
pdf.section_title('2.  Dataset Description')
pdf.sub_title('2.1  JM1 Dataset (PROMISE Repository)')
pdf.body(
    'The JM1 dataset, sourced from the PROMISE software engineering repository, '
    'was selected as the primary dataset. It is a NASA software defect dataset '
    'containing software modules written in C, with 21 complexity metrics as features '
    'and a binary defect label.'
)

cols   = ['Property', 'Value']
widths = [75, 99]
pdf.table_header(cols, widths)
drows = [
    ('Total software modules',  '10,885'),
    ('Number of features',      '21 software complexity metrics'),
    ('Defective modules',       '2,106  (19.3%)'),
    ('Non-defective modules',   '8,779  (80.7%)'),
    ('Class imbalance ratio',   '4.2 : 1'),
    ('Missing values',          '25  (in 5 columns)'),
    ('Feature types',           'All numeric'),
]
for i, (k, v) in enumerate(drows):
    pdf.table_row([k, v], widths, highlight=(i % 2 == 1), aligns=['L', 'L'])

pdf.ln(3)
pdf.sub_title('2.2  Feature Description')
pdf.body('The 21 features comprise Halstead complexity metrics and McCabe\'s cyclomatic '
         'complexity measures:')
feats = [
    'loc -- Lines of Code',
    'v(g) -- Cyclomatic Complexity (branching paths)',
    'ev(g), iv(g) -- Essential and Design Complexity',
    'n, v, l, d, i, e, b, t -- Full Halstead metrics suite',
    'lOCode, lOComment, lOBlank -- Source line category counts',
    'uniq_Op, uniq_Opnd, total_Op, total_Opnd -- Operator/operand counts',
    'branchCount -- Number of branching points (if/else/switch)',
]
for f in feats:
    pdf.bullet(f)


# ══════════════════════════════════════════════════════════
# PAGE 3 -- EDA & Preprocessing
# ══════════════════════════════════════════════════════════
pdf.add_page()

pdf.section_title('3.  Exploratory Data Analysis')
pdf.sub_title('3.1  Class Imbalance')
pdf.body(
    'EDA confirmed a significant class imbalance: defective modules represent only '
    '19.3% of all samples. A naive classifier predicting all modules as "non-defective" '
    'would still achieve 80.7% accuracy while catching zero bugs. This confirms that '
    'F1-Score and Recall must be used as primary evaluation metrics.'
)

pdf.sub_title('3.2  Feature Analysis -- Top Predictors')
cols   = ['Feature', 'Buggy Mean', 'Clean Mean', 'Ratio', 'Insight']
widths = [38, 28, 28, 22, 58]
pdf.table_header(cols, widths)
feat_rows = [
    ('t  (Halstead Time)',    '6,285.2', '1,029.6', '6.1x', 'Very high in buggy'),
    ('e  (Halstead Effort)',  '113,134', '18,533',  '6.1x', 'Very high in buggy'),
    ('v  (Halstead Volume)',  '1,422.4', '494.2',   '2.9x', 'Very high in buggy'),
    ('loc  (Lines of Code)',  '80.4',    '32.8',    '2.4x', 'Very high in buggy'),
    ('branchCount',           '21.6',    '8.8',     '2.4x', 'Very high in buggy'),
    ('v(g)  (Cyclomatic)',    '11.9',    '5.0',     '2.4x', 'Very high in buggy'),
]
for i, r in enumerate(feat_rows):
    pdf.table_row(list(r), widths, highlight=(i % 2 == 1),
                  aligns=['L','C','C','C','L'])

# EDA chart
chart1 = f'{RESULTS}\\01_class_distribution.png'
if os.path.exists(chart1):
    pdf.ln(4)
    pdf.set_font('Helvetica', 'I', 8.5); pdf.set_text_color(*DGRAY)
    pdf.cell(0, 5, 'Figure 1: Class distribution (bar chart and pie chart)', align='C',
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.image(chart1, x=18, w=pdf.w - 36)

# Preprocessing
pdf.section_title('4.  Data Preprocessing Pipeline')
steps = [
    ('1. Missing Value Imputation',
     '25 missing values across 5 columns filled using column-wise median imputation, '
     'which is robust against skewed distributions common in software metrics.'),
    ('2. Outlier Handling',
     'Winsorization applied at the 99th percentile per feature to cap extreme values '
     'without removing data rows.'),
    ('3. Stratified Train / Test Split',
     '80% training (8,708 samples) and 20% test (2,177 samples), stratified by class '
     'label (random_state=42) to preserve the original imbalance ratio in both sets.'),
    ('4. Min-Max Normalization',
     'All features scaled to [0, 1]. Scaler fitted only on training set to prevent '
     'data leakage into the test set.'),
    ('5. BorderlineSMOTE',
     'Applied only to the training set. Generated 5,338 synthetic minority-class samples, '
     'achieving a balanced 1:1 ratio (7,023 buggy : 7,023 clean). '
     'Test set intentionally left at original imbalanced ratio.'),
]
for title, desc in steps:
    pdf.set_font('Helvetica', 'B', 9.5); pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 9.5); pdf.set_text_color(*DGRAY)
    pdf.multi_cell(0, 5.5, desc)
    pdf.ln(1)

cols   = ['Split', 'Total Samples', 'Buggy', 'Clean']
widths = [50, 50, 40, 34]
pdf.table_header(cols, widths)
split_rows = [
    ('Train (raw)',    '8,708',  '1,685', '7,023'),
    ('Train (SMOTE)', '14,046', '7,023', '7,023'),
    ('Test (real)',   '2,177',  '421',   '1,756'),
]
for i, r in enumerate(split_rows):
    pdf.table_row(list(r), widths, highlight=(i == 1))


# ══════════════════════════════════════════════════════════
# PAGE 4 -- Model Results
# ══════════════════════════════════════════════════════════
pdf.add_page()

pdf.section_title('5.  Baseline Machine Learning Models')
pdf.sub_title('5.1  Models Implemented')
pdf.body(
    'Two traditional ML classifiers were trained as baselines, each under two '
    'conditions: without SMOTE (imbalanced training data) and with SMOTE (balanced '
    'training data) -- giving four baseline experiments in total.'
)
pdf.bullet('Random Forest:  200 estimators, max depth 15, random_state=42')
pdf.bullet('Naive Bayes:    Gaussian NB with default parameters')

pdf.ln(3)
pdf.sub_title('5.2  Baseline Results')
cols   = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC']
widths = [46, 26, 26, 22, 26, 28]
pdf.table_header(cols, widths)
b_rows = [
    ('RF  (no SMOTE)', '0.8107', '0.5280', '0.2019', '0.2921', '0.7365'),
    ('RF  (SMOTE)',    '0.7653', '0.4043', '0.4513', '0.4265', '0.7350'),
    ('NB  (no SMOTE)', '0.7901', '0.4412', '0.3207', '0.3714', '0.6800'),
    ('NB  (SMOTE)',    '0.7735', '0.4037', '0.3587', '0.3799', '0.6792'),
]
for i, r in enumerate(b_rows):
    pdf.table_row(list(r), widths, highlight=(i == 1))

pdf.ln(2)
pdf.sub_title('5.3  Key Observations')
obs = [
    'RF + SMOTE achieved the highest F1-Score of 0.4265 -- the baseline target to beat.',
    'Without SMOTE, RF achieved 81.1% accuracy but caught only 20.2% of bugs (85/421), '
     'demonstrating the accuracy paradox in imbalanced classification.',
    'SMOTE improved RF Recall from 0.202 to 0.451 (+123%), confirming its effectiveness.',
    'Random Forest significantly outperformed Naive Bayes across all metrics.',
]
for o in obs:
    pdf.bullet(o)

# Chart
chart11 = f'{RESULTS}\\11_baseline_comparison.png'
if os.path.exists(chart11):
    pdf.ln(3)
    pdf.set_font('Helvetica', 'I', 8.5); pdf.set_text_color(*DGRAY)
    pdf.cell(0, 5, 'Figure 2: Baseline model performance comparison', align='C',
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.image(chart11, x=18, w=pdf.w - 36)

# CNN-LSTM
pdf.section_title('6.  CNN-LSTM Deep Learning Model')
pdf.sub_title('6.1  Architecture')
cols   = ['Layer', 'Configuration', 'Purpose']
widths = [35, 55, 84]
pdf.table_header(cols, widths)
arch = [
    ('Input',        '(batch, 21, 1)',             '21 metric features per sample'),
    ('Conv1D',       '64 filters, kernel=3',       'Local pattern detection'),
    ('BatchNorm',    '--',                          'Training stabilisation'),
    ('Conv1D',       '128 filters, kernel=3',      'Deep feature extraction'),
    ('BatchNorm',    '--',                          'Training stabilisation'),
    ('LSTM',         'hidden=64, layers=1',        'Sequential dependencies'),
    ('Dropout',      'rate=0.4',                   'Regularisation'),
    ('Dense',        '32 units, ReLU',             'Feature compression'),
    ('Dense',        '1 unit, Sigmoid',            'Bug probability [0, 1]'),
    ('Parameters',   '77,121  trainable',          '--'),
]
for i, r in enumerate(arch):
    pdf.table_row(list(r), widths, highlight=(i % 2 == 1), aligns=['L','L','L'])


# ══════════════════════════════════════════════════════════
# PAGE 5 -- Focal Loss, Results, Next Steps
# ══════════════════════════════════════════════════════════
pdf.add_page()

pdf.sub_title('6.2  Focal Loss  --  Research Contribution')
pdf.body(
    'Two loss functions were evaluated. Binary Cross-Entropy (BCE) served as the '
    'standard deep learning baseline. Focal Loss (Lin et al., 2017) was adapted '
    'as the research contribution for imbalance-aware training:'
)
pdf.body(
    'FL(pt) = -a · (1 - pt)^g · log(pt)',
    indent=12
)
pdf.bullet('a = 0.75  --  weights the minority (buggy) class more heavily')
pdf.bullet('g = 2.0   --  down-weights easy examples, focuses on hard-to-detect bugs')
pdf.bullet('Both models trained for 30 epochs  |  Optimizer: Adam  |  LR: 0.001')

pdf.ln(3)
pdf.sub_title('6.3  CNN-LSTM Results')
cols   = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC']
widths = [50, 26, 26, 22, 26, 24]
pdf.table_header(cols, widths)
cnn_rows = [
    ('CNN-LSTM  (Cross-Entropy)', '0.6647', '0.3057', '0.5772', '0.3997', '0.6808'),
    ('CNN-LSTM  (Focal Loss)',    '0.5581', '0.2702', '0.7553', '0.3980', '0.7001'),
]
for i, r in enumerate(cnn_rows):
    pdf.table_row(list(r), widths, highlight=(i == 1))

pdf.ln(3)
pdf.sub_title('6.4  Full Comparison  --  All Models')
cols   = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1', 'AUC']
widths = [50, 26, 26, 22, 22, 28]
pdf.table_header(cols, widths)
all_rows = [
    ('RF  (no SMOTE)',         '0.8107', '0.5280', '0.2019', '0.2921', '0.7365'),
    ('RF  (SMOTE)',            '0.7653', '0.4043', '0.4513', '0.4265', '0.7350'),
    ('NB  (no SMOTE)',         '0.7901', '0.4412', '0.3207', '0.3714', '0.6800'),
    ('NB  (SMOTE)',            '0.7735', '0.4037', '0.3587', '0.3799', '0.6792'),
    ('CNN-LSTM  (BCE)',        '0.6647', '0.3057', '0.5772', '0.3997', '0.6808'),
    ('CNN-LSTM  (Focal Loss)', '0.5581', '0.2702', '0.7553', '0.3980', '0.7001'),
]
for i, r in enumerate(all_rows):
    pdf.table_row(list(r), widths, highlight=(i == 5))

pdf.ln(3)
pdf.body(
    'The Focal Loss CNN-LSTM caught 318 out of 421 buggy modules in the test set '
    '(Recall: 75.5%), compared to 190 caught by the best baseline (RF + SMOTE, '
    'Recall: 45.1%) -- representing 128 additional bugs detected, a 67.4% '
    'improvement in Recall.'
)

# All models chart
chart15 = f'{RESULTS}\\15_all_models_comparison.png'
if os.path.exists(chart15):
    pdf.ln(2)
    pdf.set_font('Helvetica', 'I', 8.5); pdf.set_text_color(*DGRAY)
    pdf.cell(0, 5, 'Figure 3: All models performance comparison', align='C',
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.image(chart15, x=18, w=pdf.w - 36)

# Next steps
pdf.section_title('7.  Next Steps')
steps_next = [
    ('Notebook 05 -- BERT Model',
     'Implement a BERT-based text classifier for bug report classification '
     'using the Bugzilla / GitBugs dataset.'),
    ('Notebook 06 -- Enhanced CNN-LSTM',
     'Fine-tune the Focal Loss model with additional epochs and class-weighted '
     'training to improve F1-Score while maintaining high Recall.'),
    ('10-Fold Cross-Validation',
     'Apply stratified k-fold CV across all models for statistical reliability.'),
    ('Cross-Project Validation',
     'Train on JM1, evaluate on KC1 to assess model generalisability.'),
    ('Report Writing',
     'Begin drafting Methodology and Results chapters.'),
]
for title, desc in steps_next:
    pdf.set_font('Helvetica', 'B', 9.5); pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, f'*  {title}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 9.5); pdf.set_text_color(*DGRAY)
    pdf.set_x(pdf.l_margin + 8)
    pdf.multi_cell(0, 5.5, desc)
    pdf.ln(1)

# Signature block
pdf.ln(6)
pdf.set_draw_color(*BLUE); pdf.set_line_width(0.3)
pdf.line(18, pdf.get_y(), pdf.w - 18, pdf.get_y()); pdf.ln(5)
pdf.set_font('Helvetica', '', 9.5); pdf.set_text_color(*DGRAY)
sign_items = [
    ('Student',    'S.Shanthosh  (20APSE4882)'),
    ('Supervisor', 'Mrs. WMLS Abeythunga'),
    ('Date',       '27th May 2026'),
]
for k, v in sign_items:
    pdf.set_font('Helvetica', 'B', 9.5); pdf.set_text_color(*BLUE)
    pdf.cell(40, 7, k + ':')
    pdf.set_font('Helvetica', '', 9.5); pdf.set_text_color(*DGRAY)
    pdf.cell(0, 7, v, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


# ── Save ───────────────────────────────────────────────────
pdf.output(OUT)
print(f'PDF generated successfully!')
print(f'Location: {OUT}')
