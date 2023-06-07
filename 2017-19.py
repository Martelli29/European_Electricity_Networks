import networkx as nx
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

Nations = []
TotalProduction2020 = []
CarbonDensity2020 = []

with open("Nations.txt", "r") as file:
    next(file)  # skip first row
    row = next(file)  # second row
    Nations = row.strip().split(",")

with open('ElectricityProductionTWhFINAL.txt', 'r') as file:
    TotalEnergy = csv.reader(file)
    next(TotalEnergy)   # skip first row
    for row in TotalEnergy:
        last_column = row[-1]  # select last column
        TotalProduction2020.append(last_column)
    TotalProduction2020 = list(map(float, TotalProduction2020))

a = sum(TotalProduction2020)
print(a)

with open("sharebysourceCarbonDensity.txt", "r") as file:
    contribute = csv.reader(file)
    next(file)  # skip first row
    for row in contribute:
        last_column = row[-1]  # select last column
        CarbonDensity2020.append(last_column)
    CarbonDensity2020 = list(map(float, CarbonDensity2020))

lista=[]
for i in range(len(Nations)):
    t=CarbonDensity2020[i]*TotalProduction2020[i]
    lista.append(t)

pes=sum(lista)/a    
print(pes)

G = nx.DiGraph()


def NodeConstruction():
    for i in range(len(Nations)):
        G.add_node(str(Nations[i]))


pos = {'ALB': (1.1, -3), 'AUT': (0.3, -1), 'BIH': (0.7, -2), 'BEL': (-0.8, 0.5), 'BGR': (2.5, -2.5), 'BLR': (2.2, 1), 'CHE': (-0.3, -1), 'CZE': (0.5, -0.5), 'DEU': (0, 0), 'DNK': (0, 2), 'EST': (2, 2.5), 'ESP': (-1.5, -2), 'FIN': (2, 3.5), 'FRA': (-1, -1), 'GBR': (-2, 2.5), 'GRC': (1.3, -3.6), 'HRV': (0.8, -1.5), 'HUN': (1.5, -1), 'IRL': (-2.5, 2.5),
       'ITA': (0, -2), 'LTU': (2, 1.5), 'LUX': (-0.5, 0), 'LVA': (2, 2), 'MDA': (3, -1), 'MNE': (0.9, -2.5), 'MKD': (1.5, -3), 'MLT': (0, -3), 'NLD': (-0.5, 1), 'NOR': (0, 3.5), 'POL': (1.3, 0.2), 'PRT': (-2.5, -2), 'ROU': (2.5, -1), 'SRB': (1.5, -2.2), 'RUS': (3.7, 2.5), 'SWE': (1, 2.5), 'SVN': (0.6, -1.2), 'SVK': (1, -0.5), 'TUR': (3.5, -3.5), 'UKR': (3, 0.5)}

NodeConstruction()

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
        ColorMap.append("red")
    elif CarbonDensity2020[i] >= 500:
        ColorMap.append("brown")


matrix = np.zeros((len(G.nodes), len(G.nodes)))


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

Edges = []
AdjMat = np.zeros((len(G.nodes), len(G.nodes)))
for i in range(len(G)):
    for j in range(len(G)):
        if i < j:
            if matrix[i][j] != 0.0 or matrix[j][i] != 0.0:
                if matrix[i][j]-matrix[j][i] >= 0:
                    Edges.append(
                        (Nations[i], Nations[j], (matrix[i][j]-matrix[j][i])))
                else:
                    Edges.append(
                        (Nations[j], Nations[i], (matrix[j][i]-matrix[i][j])))
            else:
                pass
        else:
            pass


G.add_weighted_edges_from(Edges)
degree_dict = dict(G.degree(G.nodes()))






#bc = nx.betweenness_centrality(G, normalized=True, endpoints=True, weight='weight')
#print(bc) #non so se è utile

# closeness_centrality = nx.closeness_centrality(G, distance='weight', wf_improved=True)
# print(closeness_centrality) #non so se è utile

#hits=nx.hits(G, max_iter=100, tol=1e-15, nstart=None, normalized=True)
#print(hits)


edge_weights = [G[u][v]['weight']/400000 for u, v in G.edges()]

nx.draw(G, pos=pos, node_size=[
        x * 8 for x in TotalProduction2020], node_color=ColorMap, with_labels=True, font_size=8, width=edge_weights)


plt.show()
# degree fatto
# matrice al quadrato
# centralità di flusso, ho foto su cell
# centralità di intermediazione di flusso
# resistenza di flusso
# pagerank?



