import networkx as nx
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

Nations = []
TotalProduction2020 = []
CarbonDensity2020 = []

with open("Nations.txt", "r") as file:
    next(file)  # salta la prima riga
    row = next(file)  # stampa la seconda riga
    Nations = row.strip().split(",")

with open('Electricity_Production_TWh2020_FINAL.txt', 'r') as file:
    TotalEnergy = csv.reader(file)
    next(TotalEnergy)
    for row in TotalEnergy:
        last_column = row[-1]  # seleziona l'ultima colonna
        TotalProduction2020.append(last_column)
    TotalProduction2020 = list(map(float, TotalProduction2020))


with open("share-by-source2020+Carbon_Density.txt", "r") as file:
    contribute = csv.reader(file)
    next(file)  # skip first row
    for row in contribute:
        last_column = row[-1]  # seleziona l'ultima colonna
        CarbonDensity2020.append(last_column)
    CarbonDensity2020 = list(map(float, CarbonDensity2020))


G = nx.DiGraph()

for i in range(len(Nations)):
    G.add_node(str(Nations[i]))

ColorMap = []
for i in range(len(G)):
    if CarbonDensity2020[i] < 100.0:
        ColorMap.append("green")
    elif CarbonDensity2020[i] >= 100 and CarbonDensity2020[i] < 200:
        ColorMap.append("lightgreen")
    elif CarbonDensity2020[i] >= 200 and CarbonDensity2020[i] < 300:
        ColorMap.append("yellow")
    elif CarbonDensity2020[i] >= 300 and CarbonDensity2020[i] < 400:
        ColorMap.append("orange")
    elif CarbonDensity2020[i] >= 400 and CarbonDensity2020[i] < 500:
        ColorMap.append("brown")
    elif CarbonDensity2020[i] >= 500:
        ColorMap.append("black")


matrix = np.zeros((len(G.nodes), len(G.nodes)))
df = pd.read_csv("Imp-Exp_2017-19.txt")


def FillMatrix():
    df = pd.read_csv("Imp-Exp_2017-19.txt")
    for i in range(len(G.nodes)):
        for j in range(len(G.nodes)):
            if not df.loc[(df['source'] == Nations[i]) & (df['target'] == Nations[j])].empty:
                matrix[i][j] = df.loc[(df['source'] == Nations[i]) & (
                df['target'] == Nations[j]), 'value'].iloc[0]
            else:
                pass

FillMatrix()
print(matrix)
# nx.draw(G, node_size=[x * 20 for x in TotalProduction2020], node_color=ColorMap, with_labels=True)
# plt.show()

'''
fig, ax = plt.subplots(figsize=(10, 10))
im = ax.imshow(matrix, cmap='viridis')

# mostra la barra colori
cbar = ax.figure.colorbar(im, ax=ax)

# impostazioni degli assi
ax.set_xticks(range(len(G.nodes)))
ax.set_yticks(range(len(G.nodes)))
ax.set_xticklabels(Nations2020, rotation=90)
ax.set_yticklabels(Nations2020)

# aggiungi etichette agli assi
ax.set_xlabel("Target")
ax.set_ylabel("Source")
ax.set_title("Matrice di flusso")

# mostra l'immagine

plt.show()
'''
#np.savetxt("matrix.txt", matrix)
