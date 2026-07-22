content = open('report/generate_pdf.py', encoding='utf-8').read()
replacements = [
    ('—', '--'),   # em dash
    ('–', '-'),    # en dash
    ('’', "'"),    # right single quote
    ('‘', "'"),    # left single quote
    ('“', '"'),    # left double quote
    ('”', '"'),    # right double quote
    ('•', '*'),    # bullet
    ('α', 'a'),    # alpha
    ('γ', 'g'),    # gamma
    ('₁', '1'),    # subscript 1
    ('ₜ', 't'),    # subscript t
]
for old, new in replacements:
    content = content.replace(old, new)
with open('report/generate_pdf.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
