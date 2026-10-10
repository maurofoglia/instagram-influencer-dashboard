import nbformat as nbf

notebook_path = 'notebooks/01_EDA_and_Preprocessing.ipynb'
try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)
except Exception as e:
    print(f"Error reading notebook: {e}")
    exit(1)

new_code = """\
# Mappiamo i nomi temporanei con le vere categorie di Business
nomi_reali = {
    'Tipo C': 'Top Performer (Alta Interazione)',
    'Tipo A': 'Promettenti (Media Interazione)',
    'Tipo D': 'Standard (Bassa Interazione)',
    'Tipo B': 'Mega Celebrità (Tanti Follower, Interazione Bassa)'
}

# Creiamo la colonna finale
df_model['Segmento'] = df_model['cluster_name'].map(nomi_reali)

# Selezioniamo le colonne utili per la Dashboard
colonne_finali = [
    'influencer_insta_name', 'instagram_name', 'category_1', 
    'followers', 'audience_country(mostly)', 'authentic_engagement', 
    'engagement_avg', 'engagement_rate', 'Segmento'
]
df_finale = df_model[colonne_finali]

# Esportiamo il dataset arricchito e pulito!
df_finale.to_csv('../data/processed/influencers_segmented.csv', index=False)
print("File esportato con successo in data/processed/influencers_segmented.csv!")
"""

# Trova la cella di execute esistente e sovrascrivila
for cell in nb.cells:
    if cell.cell_type == 'code' and 'df.to_csv' in cell.source and 'influencers_cleaned.csv' in cell.source:
        cell.source = new_code
        break

try:
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Execute cell updated successfully.")
except Exception as e:
    print(f"Error writing notebook: {e}")
