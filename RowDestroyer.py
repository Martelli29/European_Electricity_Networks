import pandas as pd

df = pd.read_csv('share-elec-produc-by-source.txt')
df = df[df["Year"].isin([2017, 2018, 2019])]
print(df)
df.to_csv('share-elec-produc-by-source-FILTERED.txt', index=False)