import nbformat as nbf
notebook_path = 'notebooks/01_EDA_and_Preprocessing.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

construct_md = """\
# PACE Framework: Construct Stage
**Objective:** Engineer new features and build analytical models.

1. **Feature Engineering:** We will calculate the `engagement_rate`.
2. **Segmentation Model:** We will use a Machine Learning algorithm called **K-Means Clustering** to segment influencers into 4 distinct business categories based on their followers and engagement rate.
"""

construct_code1 = """\
from sklearn.cluster import KMeans

# 1. Feature Engineering: Engagement Rate
df['engagement_rate'] = df['engagement_avg'] / df['followers']

# Remove extreme outliers that might be data anomalies (Engagement Rate > 100%)
df_model = df[df['engagement_rate'] <= 1.0].copy()

# 2. Machine Learning: K-Means Clustering
# We will segment the influencers into 4 clusters.
X = df_model[['followers', 'engagement_rate']]

# Initialize and fit the K-Means model
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_model['cluster'] = kmeans.fit_predict(X)

# Map the generic cluster numbers to business segments based on cluster centers.
centers = kmeans.cluster_centers_
# centers[:, 0] = followers, centers[:, 1] = engagement_rate

def map_clusters(df_clustered, centers):
    mapping = {}
    for i, center in enumerate(centers):
        if center[0] > 1.5e7 and center[1] >= 0.04:
            mapping[i] = 'Stars (High Follower, High Interaction)'
        elif center[0] > 1.5e7 and center[1] < 0.04:
            mapping[i] = 'Celebrities (High Follower, Low Interaction)'
        elif center[0] <= 1.5e7 and center[1] >= 0.04:
            mapping[i] = 'Active Niche (Micro-Infl. High Interaction)'
        else:
            mapping[i] = 'Low Potential (Micro-Infl. Low Interaction)'
    return df_clustered['cluster'].map(mapping)

df_model['Segmento'] = map_clusters(df_model, centers)

# Visualize the Segmentation Matrix
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_model, x='followers', y='engagement_rate', hue='Segmento', palette='Set1', alpha=0.7)
plt.title('Influencer Business Segmentation Matrix (K-Means)')
plt.xlabel('Followers')
plt.ylabel('Engagement Rate')
plt.show()

print("Number of Influencers per Segment:")
display(df_model['Segmento'].value_counts())
"""

nb.cells[8].source = construct_md
nb.cells[9].source = construct_code1

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print("Notebook Construct stage updated to use KMeans!")
