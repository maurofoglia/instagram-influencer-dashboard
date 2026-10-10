import nbformat as nbf

notebook_path = 'notebooks/01_EDA_and_Preprocessing.ipynb'
try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)
except Exception as e:
    print(f"Error reading notebook: {e}")
    exit(1)

new_code = """\
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 1. Selezioniamo le feature per il modello (Followers ed Engagement Rate)
features = df[['followers', 'engagement_rate']].copy()

# 2. Rimuoviamo eventuali outlier estremi dell'engagement rate (es. rate > 1.0)
features = features[features['engagement_rate'] <= 1.0] 
df_model = df.loc[features.index].copy()

# 3. Standardizziamo i dati
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# 4. Addestriamo il modello K-Means con 4 cluster
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_model['cluster'] = kmeans.fit_predict(features_scaled)

# Mappiamo i cluster con dei nomi leggibili (questo aiuterà nella dashboard)
# Nota: I nomi dipendono da come l'algoritmo ordina i cluster, qui diamo un nome provvisorio
cluster_names = {0: 'Tipo A', 1: 'Tipo B', 2: 'Tipo C', 3: 'Tipo D'}
df_model['cluster_name'] = df_model['cluster'].map(cluster_names)

# 5. Visualizziamo i cluster creati
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_model, x='followers', y='engagement_rate', hue='cluster_name', palette='Set1', alpha=0.7)
plt.title('Segmentazione Influencer (K-Means)')
plt.xlabel('Followers')
plt.ylabel('Engagement Rate')
plt.show()

print("Numero di influencer per ogni Cluster:")
display(df_model['cluster_name'].value_counts())
"""
new_cell = nbf.v4.new_code_cell(new_code)

# Find where to insert it: before the "Execute Stage" markdown
insert_idx = len(nb.cells)
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'markdown' and 'pacE: Execute Stage' in cell.source:
        insert_idx = i
        break

nb.cells.insert(insert_idx, new_cell)

try:
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("K-Means cell inserted successfully.")
except Exception as e:
    print(f"Error writing notebook: {e}")
