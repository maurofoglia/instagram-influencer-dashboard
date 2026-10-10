import pandas as pd

df = pd.read_csv('data/raw/instagram_influencers.csv')
print("Columns:")
print(df.columns.tolist())
print("\nFirst 3 rows:")
print(df.head(3))
print("\nInfo:")
print(df.info())
