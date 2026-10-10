import nbformat as nbf

nb = nbf.v4.new_notebook()

# ================================
# PACE: Plan
# ================================
plan_md = """\
# PACE Framework: Plan Stage
**Business Scenario & Objective:**
The marketing department is looking to launch a global influencer campaign. However, they are unsure how to identify the most valuable creators. Mega-celebrities are expensive, but do they actually guarantee high audience interaction? 
Our goal in this project is to analyze a dataset of top Instagram influencers, perform data cleaning, and use analytical models to segment them into actionable business categories.

In this **Plan Stage**, we will:
1. Load the raw data.
2. Gather basic information and understand the variables.
3. Clean the dataset (fix column names, convert string metrics to numbers, and handle missing data).
"""

plan_code1 = """\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set a clean aesthetic for our plots
sns.set_theme(style="whitegrid")

# 1. Load the raw dataset
df = pd.read_csv('../data/raw/instagram_influencers.csv')

# Let's take a look at the first few rows to understand the structure
display(df.head())

# Gather descriptive statistics and data types
display(df.info())
"""

plan_code2 = """\
# 2. Data Cleaning: Column Names
# Initial Observation: The column names contain spaces, uppercase letters, and hidden newline characters (like '\\r\\n').
# We need to standardize them to 'snake_case' for easier coding.
df.columns = (df.columns
                .str.replace(r'\\n|\\r', '', regex=True)
                .str.strip()
                .str.replace(' ', '_')
                .str.lower())

print("Standardized Column Names:")
print(df.columns.tolist())
"""

plan_code3 = """\
# 3. Data Cleaning: Numeric Conversions
# Initial Observation: 'followers' and 'engagement_avg' are stored as strings (objects) because they contain 'M' (Millions) and 'K' (Thousands).
# We must convert these to actual floating-point numbers to perform statistical analysis.

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

# Explicitly rename columns just in case invisible characters persisted
df.rename(columns={
    'authentic_engagement\\r\\n': 'authentic_engagement',
    'engagement_avg\\r\\n': 'engagement_avg'
}, inplace=True, errors='ignore')

cols_to_convert = ['followers', 'authentic_engagement', 'engagement_avg']
for col in cols_to_convert:
    if col in df.columns:
        df[col] = df[col].apply(convert_to_number)

# Verify the transformations
display(df.head(3))
"""

plan_code4 = """\
# 4. Data Cleaning: Missing Values and Duplicates
print("Missing values per column:")
display(df.isna().sum())

# Observation: 'category_2' is missing over 70% of its data. 'category_1' and 'audience_country' have minor missing values.
# Instead of dropping valuable rows, we will impute categorical missing values with the label 'Unknown'.

df['category_1'] = df['category_1'].fillna('Unknown')
df['category_2'] = df['category_2'].fillna('Unknown')
df['audience_country(mostly)'] = df['audience_country(mostly)'].fillna('Unknown')
df['instagram_name'] = df['instagram_name'].fillna('Unknown')

# Check and drop duplicate rows
duplicates = df.duplicated().sum()
print(f"\\nFound {duplicates} duplicate rows. Dropping them...")
df = df.drop_duplicates()

print("Missing values after imputation:")
display(df.isna().sum())
"""

# ================================
# PACE: Analyze
# ================================
analyze_md = """\
# PACE Framework: Analyze Stage
**Objective:** Perform Exploratory Data Analysis (EDA) to uncover relationships between variables.

*Key Questions:*
- How are followers distributed? Is it a normal distribution or skewed?
- Are there extreme outliers in engagement?
- Does having more followers automatically translate to higher average engagement?
"""

analyze_code1 = """\
# Distribution of Followers
# We use a histogram to visualize the spread of followers.
plt.figure(figsize=(10, 5))
sns.histplot(df['followers'], bins=50, kde=True)
plt.title('Distribution of Followers')
plt.xlabel('Followers')
plt.ylabel('Frequency')
plt.show()

# Insight: The distribution is heavily right-skewed. The vast majority of influencers have under 50 Million followers, 
# while a long tail extends towards 500 Million (Mega-Celebrities).

# Detecting Outliers in Average Engagement
plt.figure(figsize=(10, 2))
sns.boxplot(x=df['engagement_avg'])
plt.title('Boxplot of Average Engagement')
plt.show()

# Insight: The boxplot shows the interquartile range squished far to the left. The dots stretching to the right are extreme outliers 
# indicating rare accounts with phenomenally high engagement.
"""

analyze_code2 = """\
# Relationship between Followers and Average Engagement
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='followers', y='engagement_avg', alpha=0.5)
plt.title('Followers vs Average Engagement')
plt.xlabel('Followers')
plt.ylabel('Average Engagement')
plt.show()

# Insight: There is NO strong linear correlation. The influencer with the highest engagement (~20M) only has around 40M followers. 
# Conversely, the account with 500M followers has near-zero relative engagement. 
# Conclusion: Raw numbers are misleading. We must calculate a normalized metric: the 'Engagement Rate'.
"""

# ================================
# PACE: Construct
# ================================
construct_md = """\
# PACE Framework: Construct Stage
**Objective:** Engineer new features and build analytical models.

1. **Feature Engineering:** We will calculate the `engagement_rate`.
2. **Segmentation Model:** Since we cannot use Scikit-Learn's K-Means due to a Windows Defender environment restriction on the C++ DLL, 
we will implement a highly interpretable **Rule-Based Matrix Segmentation** using pure Pandas. We'll categorize influencers based on median thresholds.
"""

construct_code1 = """\
# 1. Feature Engineering: Engagement Rate
df['engagement_rate'] = df['engagement_avg'] / df['followers']

# Remove extreme outliers that might be data anomalies (Engagement Rate > 100%)
df_model = df[df['engagement_rate'] <= 1.0].copy()

# 2. Rule-Based Segmentation
# Based on earlier EDA, the median followers are ~15 Million and median engagement rate is ~4%.
# We will use these thresholds to construct a 4-quadrant business matrix.

def assign_segment(row):
    if row['followers'] >= 15000000 and row['engagement_rate'] >= 0.04:
        return 'Stars (High Follower, High Interaction)'
    elif row['followers'] >= 15000000 and row['engagement_rate'] < 0.04:
        return 'Celebrities (High Follower, Low Interaction)'
    elif row['followers'] < 15000000 and row['engagement_rate'] >= 0.04:
        return 'Active Niche (Micro-Infl. High Interaction)'
    else:
        return 'Low Potential (Micro-Infl. Low Interaction)'

df_model['Segmento'] = df_model.apply(assign_segment, axis=1)

# Visualize the Segmentation Matrix
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_model, x='followers', y='engagement_rate', hue='Segmento', palette='Set1', alpha=0.7)
plt.title('Influencer Business Segmentation Matrix')
plt.xlabel('Followers')
plt.ylabel('Engagement Rate')
plt.show()

print("Number of Influencers per Segment:")
display(df_model['Segmento'].value_counts())
"""

# ================================
# PACE: Execute
# ================================
execute_md = """\
# PACE Framework: Execute Stage
**Objective:** Interpret results, summarize key insights for stakeholders, and export the finalized dataset for the interactive Streamlit Dashboard.

*Key Business Recommendations:*
- **Active Niche Creators** are highly valuable: they are likely cheaper to sponsor but yield excellent engagement rates.
- **Celebrities** should be used strictly for broad Brand Awareness, not for direct conversion or high-engagement campaigns.
- Further geospatial analysis and Bot Detection will be handled dynamically in the Streamlit application.
"""

execute_code1 = """\
# Select only the relevant columns for our Dashboard to optimize memory and speed
final_columns = [
    'influencer_insta_name', 'instagram_name', 'category_1', 
    'followers', 'audience_country(mostly)', 'authentic_engagement', 
    'engagement_avg', 'engagement_rate', 'Segmento'
]
df_final = df_model[final_columns]

# Export the clean, enriched dataset
df_final.to_csv('../data/processed/influencers_segmented.csv', index=False)
print("Data successfully exported to data/processed/influencers_segmented.csv!")
print("The data is now ready to be consumed by the Streamlit Dashboard (src/app.py).")
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
print("English Notebook updated successfully.")
