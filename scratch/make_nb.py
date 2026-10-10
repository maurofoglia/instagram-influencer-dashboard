import nbformat as nbf

nb = nbf.v4.new_notebook()

text = """\
# EDA & Preprocessing - Instagram Influencers
Benvenuti nel primo notebook di Exploratory Data Analysis.
In questo notebook effettueremo il caricamento dei dati e la pulizia delle colonne.\
"""

code = """\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Impostiamo lo stile dei grafici
sns.set_theme(style="whitegrid")

# 1. Caricamento del dataset
df = pd.read_csv('../data/raw/instagram_influencers.csv')

# 2. Pulizia nomi delle colonne (rimuove spazi vuoti, ritorni a capo e converte in minuscolo)
df.columns = (df.columns
                .str.replace(r'\\n|\\r', '', regex=True)
                .str.strip()
                .str.replace(' ', '_')
                .str.lower())

print("Nomi delle colonne sistemati:")
print(df.columns.tolist())
"""

code2 = """\
# 3. Funzione per convertire 'K' (migliaia) e 'M' (milioni) in numeri reali
def convert_to_number(val):
    if pd.isna(val):
        return val
    val = str(val).upper().replace(',', '')
    if 'M' in val:
        return float(val.replace('M', '')) * 1000000
    elif 'K' in val:
        return float(val.replace('K', '')) * 1000
    else:
        return float(val)

# Rinomina colonne problematiche (nel caso in cui \\r\\n non sia stato rimosso per intero)
df.rename(columns={
    'authentic_engagement\\r\\n': 'authentic_engagement',
    'engagement_avg\\r\\n': 'engagement_avg'
}, inplace=True, errors='ignore')

cols_to_convert = ['followers', 'authentic_engagement', 'engagement_avg']

for col in cols_to_convert:
    if col in df.columns:
        df[col] = df[col].apply(convert_to_number)

# Diamo un'occhiata ai primi record
display(df.head())
"""

code3 = """\
# 4. Statistiche descrittive
display(df.describe())

# Verifica dei valori nulli
print("\\nValori Nulli per colonna:")
print(df.isnull().sum())
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text),
    nbf.v4.new_code_cell(code),
    nbf.v4.new_code_cell(code2),
    nbf.v4.new_code_cell(code3)
]

nbf.write(nb, 'notebooks/01_EDA_and_Preprocessing.ipynb')
print("Notebook created successfully.")
