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

Weights = []

for i in range(len(G)):
    for j in range(len(G)):
        if i < j:
            if matrix[i][j] != 0.0 or matrix[j][i] != 0.0:
                Weights.append(matrix[i][j]-matrix[j][i])
            else:
                pass
        else:
            pass

Edges = []
AdjMat = np.zeros((len(G.nodes), len(G.nodes)))
for i in range(len(G)):
    for j in range(len(G)):
        if i < j:
            if matrix[i][j] != 0.0 or matrix[j][i] != 0.0:
                if matrix[i][j]-matrix[j][i] >= 0:
                    Edges.append(
                        (Nations[i], Nations[j], (matrix[i][j]-matrix[j][i])))
                    AdjMat[i][j] = matrix[i][j]-matrix[j][i]
                else:
                    Edges.append(
                        (Nations[j], Nations[i], (matrix[j][i]-matrix[i][j])))
                    AdjMat[j][i] = matrix[j][i]-matrix[i][j]
            else:
                pass
        else:
            pass


G.add_weighted_edges_from(Edges)
degree_dict = dict(G.degree(G.nodes()))


# bc = nx.betweenness_centrality(G, normalized=True, endpoints=True, weight='weight')
# print(bc) #non so se è utile

# closeness_centrality = nx.closeness_centrality(G, distance='weight', wf_improved=True)
# print(closeness_centrality) #non so se è utile


pos = nx.fruchterman_reingold_layout(G)

nx.draw(G, pos=pos, node_size=[
        x * 5 for x in TotalProduction2020], node_color=ColorMap, with_labels=True)


plt.show()

# degree fatto
# matrice al quadrato
# centralità di flusso, ho foto su cell
# centralità di intermediazione di flusso
# resistenza di flusso
# pagerank?
