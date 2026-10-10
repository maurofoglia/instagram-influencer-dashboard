import nbformat as nbf

notebook_path = 'notebooks/01_EDA_and_Preprocessing.ipynb'
try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)
except Exception as e:
    print(f"Error reading notebook: {e}")
    exit(1)

new_code = """\
# 5. Gestione dei valori mancanti
# Riempiamo i valori mancanti (NaN) con l'etichetta 'Unknown'
df['category_1'] = df['category_1'].fillna('Unknown')
df['category_2'] = df['category_2'].fillna('Unknown')
df['audience_country(mostly)'] = df['audience_country(mostly)'].fillna('Unknown')
df['instagram_name'] = df['instagram_name'].fillna('Unknown')

print("Valori mancanti dopo il fill:")
display(df.isna().sum())
"""
new_cell = nbf.v4.new_code_cell(new_code)

# Find where to insert it: before the "Analyze Stage" markdown
insert_idx = len(nb.cells)
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'markdown' and 'pAce: Analyze Stage' in cell.source:
        insert_idx = i
        break

nb.cells.insert(insert_idx, new_cell)

try:
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Cell inserted successfully.")
except Exception as e:
    print(f"Error writing notebook: {e}")
