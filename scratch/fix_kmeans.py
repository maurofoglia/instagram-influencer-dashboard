import nbformat as nbf
notebook_path = 'notebooks/01_EDA_and_Preprocessing.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

construct_md = """\
# PACE Framework: Construct Stage
**Objective:** Engineer new features and build analytical models.

1. **Feature Engineering:** We will calculate the `engagement_rate`.
2. **Segmentation Model:** We will use a Machine Learning algorithm called **K-Means Clustering** to segment influencers into 4 distinct business categories based on their followers and engagement rate.

*Crucial Note on Machine Learning:* Because 'followers' are in the tens of millions, while 'engagement_rate' is a small decimal (e.g., 0.05), the K-Means distance calculation would be completely dominated by the followers axis. To fix this, we MUST use a `StandardScaler` to normalize the data before clustering, ensuring both metrics carry equal weight.
"""

construct_code1 = """\
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 1. Feature Engineering: Engagement Rate
df['engagement_rate'] = df['engagement_avg'] / df['followers']

# Remove extreme outliers that might be data anomalies (Engagement Rate > 100%)
df_model = df[df['engagement_rate'] <= 1.0].copy()

# 2. Machine Learning: K-Means Clustering
# We will segment the influencers into 4 clusters.
X = df_model[['followers', 'engagement_rate']]

# CRITICAL FIX: Standardize the features! 
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Initialize and fit the K-Means model on the SCALED data
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_model['cluster'] = kmeans.fit_predict(X_scaled)

# Map the generic cluster numbers to business segments.
# We determine the "personality" of each cluster by looking at its median values.
cluster_summary = df_model.groupby('cluster')[['followers', 'engagement_rate']].median()
followers_median = df_model['followers'].median()
er_median = df_model['engagement_rate'].median()

mapping = {}
for cluster_id, row in cluster_summary.iterrows():
    if row['followers'] > followers_median and row['engagement_rate'] > er_median:
        mapping[cluster_id] = 'Stars (High Follower, High Interaction)'
    elif row['followers'] > followers_median and row['engagement_rate'] <= er_median:
        mapping[cluster_id] = 'Celebrities (High Follower, Low Interaction)'
    elif row['followers'] <= followers_median and row['engagement_rate'] > er_median:
        mapping[cluster_id] = 'Active Niche (Micro-Infl. High Interaction)'
    else:
        mapping[cluster_id] = 'Low Potential (Micro-Infl. Low Interaction)'

# If the algorithm found multiple clusters in the same "business quadrant", 
# we append the cluster ID to keep them distinct.
unique_mapping = {}
used_names = set()
for c_id, name in mapping.items():
    if name in used_names:
        unique_mapping[c_id] = f"{name} - Tier {c_id}"
    else:
        unique_mapping[c_id] = name
        used_names.add(name)

df_model['Segmento'] = df_model['cluster'].map(unique_mapping)

# Visualize the Segmentation Matrix
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_model, x='followers', y='engagement_rate', hue='Segmento', palette='Set1', alpha=0.7)
plt.title('Influencer Business Segmentation Matrix (K-Means)')
plt.xlabel('Followers')
plt.ylabel('Engagement Rate')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

print("Number of Influencers per Segment:")
display(df_model['Segmento'].value_counts())
"""

nb.cells[8].source = construct_md
nb.cells[9].source = construct_code1

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print("Notebook Construct stage updated with StandardScaler!")
