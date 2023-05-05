import pandas as pd

# Leggi il file CSV in un DataFrame
df = pd.read_csv('Flow_graph_2017-19.txt')
df.fillna(0, inplace=True)

# Comprimi le righe in base alle colonne 2 e 3 e calcola la media della colonna 4
df_grouped = df.groupby(['source', 'target'], as_index=False)['value'].mean()

# Visualizza il risultato

df_grouped.to_csv('Imp-Exp_2017-19.txt', index=False)





# Leggi il file CSV in un DataFrame
df = pd.read_csv('Flow_graph_2020.txt')
df.fillna(0, inplace=True)

# Comprimi le righe in base alle colonne 2 e 3 e calcola la media della colonna 4
df_grouped = df.groupby(['source', 'target'], as_index=False)['value'].mean()

# Visualizza il risultato

df_grouped.to_csv('Imp-Exp_2020.txt', index=False)