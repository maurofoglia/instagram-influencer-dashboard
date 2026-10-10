import nbformat as nbf

nb = nbf.v4.new_notebook()

# PACE: Plan
plan_md = """\
# PACE: Plan
In questa fase imposteremo l'ambiente, caricheremo i dati ed effettueremo una prima pulizia e analisi esplorativa (controllo valori nulli, duplicati, outlier)."""

plan_code1 = """\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Setup stile grafico
sns.set_theme(style="whitegrid")

# 1. Caricamento del dataset e prima esplorazione
df = pd.read_csv('../data/raw/instagram_influencers.csv')

# Mostriamo le prime righe del dataset per capire com'è strutturato
display(df.head())

# Mostriamo le informazioni generali (tipi di dato e valori non nulli)
display(df.info())
"""

plan_code2 = """\
# 2. Pulizia nomi delle colonne
# Come si nota, i nomi delle colonne hanno spazi e ritorni a capo (es. 'authentic_engagement\\r\\n'). Li puliamo.
df.columns = (df.columns
                .str.replace(r'\\n|\\r', '', regex=True)
                .str.strip()
                .str.replace(' ', '_')
                .str.lower())

print("Nomi colonne sistemati:")
print(df.columns.tolist())
"""

plan_code3 = """\
# 3. Pulizia dei dati: Conversione di 'K' e 'M' in numeri reali
# Da df.info() vediamo che 'followers' e 'engagement_avg' sono oggetti (stringhe) perché contengono le lettere.
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

# Rinominiamo esplicitamente se sono rimasti residui invisibili nei nomi
df.rename(columns={
    'authentic_engagement\\r\\n': 'authentic_engagement',
    'engagement_avg\\r\\n': 'engagement_avg'
}, inplace=True, errors='ignore')

cols_to_convert = ['followers', 'authentic_engagement', 'engagement_avg']
for col in cols_to_convert:
    if col in df.columns:
        df[col] = df[col].apply(convert_to_number)

# Verifichiamo che ora siano numeri
display(df.head())
"""

plan_code4 = """\
# 4. Controllo valori mancanti e duplicati
print("Valori mancanti per colonna:")
display(df.isna().sum())

print("\\nNumero di righe duplicate:", df.duplicated().sum())
# Rimuoviamo eventuali duplicati
df = df.drop_duplicates()
"""

# PACE: Analyze
analyze_md = """\
# pAce: Analyze Stage
Analisi Esplorativa dei Dati (EDA). Esamineremo le distribuzioni e le relazioni tra le variabili (es. Followers vs Engagement)."""

analyze_code1 = """\
# Distribuzione dei Followers
plt.figure(figsize=(10, 5))
sns.histplot(df['followers'], bins=50, kde=True)
plt.title('Distribuzione dei Followers')
plt.xlabel('Followers')
plt.ylabel('Frequenza')
plt.show()

# Boxplot per identificare outlier nell'engagement
plt.figure(figsize=(10, 2))
sns.boxplot(x=df['engagement_avg'])
plt.title('Boxplot dell\\'Engagement Medio')
plt.show()
"""

analyze_code2 = """\
# Relazione tra Followers ed Engagement Medio
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='followers', y='engagement_avg', alpha=0.5)
plt.title('Followers vs Engagement Medio')
plt.xlabel('Followers')
plt.ylabel('Engagement Medio')
plt.show()
"""

# PACE: Construct
construct_md = """\
# paCe: Construct Stage
Sviluppo dei modelli. Potremmo calcolare l'Engagement Rate (Engagement / Followers) e creare un modello di regressione per prevederlo, oppure usare il clustering (es. K-Means) per segmentare gli influencer."""

construct_code1 = """\
# Feature Engineering: Calcolo dell'Engagement Rate
df['engagement_rate'] = df['engagement_avg'] / df['followers']

# Prepariamo i dati per un eventuale clustering
# ... (il codice verrà implementato nel prossimo step) ...
"""

# PACE: Execute
execute_md = """\
# pacE: Execute Stage
Interpretazione dei risultati, riepilogo degli insight chiave per il business e preparazione dei dati per la Dashboard (es. esportazione del dataset pulito)."""

execute_code1 = """\
# Salvataggio del dataset pulito per la Dashboard
# df.to_csv('../data/processed/influencers_cleaned.csv', index=False)
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(plan_md),
    nbf.v4.new_code_cell(plan_code1),
    nbf.v4.new_code_cell(plan_code2),
    nbf.v4.new_code_cell(plan_code3),
    nbf.v4.new_code_cell(plan_code4),
    nbf.v4.new_markdown_cell(analyze_md),
    nbf.v4.new_code_cell(analyze_code1),
    nbf.v4.new_code_cell(analyze_code2),
    nbf.v4.new_markdown_cell(construct_md),
    nbf.v4.new_code_cell(construct_code1),
    nbf.v4.new_markdown_cell(execute_md),
    nbf.v4.new_code_cell(execute_code1)
]

nbf.write(nb, 'notebooks/01_EDA_and_Preprocessing.ipynb')
print("Notebook updated successfully.")
