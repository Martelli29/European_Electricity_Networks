import networkx as nx
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np


TotalProduction2020 = []
CarbonDensity2020 = []


'''This function get the names of the nodes of the network'''


def GetName():
    nations = []
    with open("Nations.txt", "r") as file:
        next(file)  # skip first row
        row = next(file)  # second row
        nations = row.strip().split(",")  # get name of the nations from the file
    return nations


Nations = GetName()

'''in this file we get the values of electricity production for each state'''
with open('Electricity_Production_TWh2020_FINAL.txt', 'r') as file:
    TotalEnergy = csv.reader(file)
    next(TotalEnergy)
    for row in TotalEnergy:
        last_column = row[-1]  # seleziona l'ultima colonna
        TotalProduction2020.append(last_column)
    TotalProduction2020 = list(map(float, TotalProduction2020))

a = sum(TotalProduction2020)
a = round(a, 2)
print("Total production is:", a)

'''in this file we get the values of the carbon intensity of the electricity generation for each state'''
with open("share-by-source2020+Carbon_Density.txt", "r") as file:
    contribute = csv.reader(file)
    next(file)  # skip first row
    for row in contribute:
        last_column = row[-1]  # seleziona l'ultima colonna
        CarbonDensity2020.append(last_column)
    CarbonDensity2020 = list(map(float, CarbonDensity2020))

lista = []
for i in range(len(Nations)):
    t = CarbonDensity2020[i]*TotalProduction2020[i]
    lista.append(t)

pes = sum(lista)/a
pes = round(pes, 2)
print("Mean carbon density is:", pes)

G = nx.DiGraph()  # inizialization of the graph


def NodeConstruction():  # construction of the node with the name of the states
    for i in range(len(Nations)):
        G.add_node(str(Nations[i]))


pos = {'ALB': (1.1, -3.1), 'AUT': (0.3, -1.3), 'BIH': (0.7, -2.5), 'BEL': (-0.9, 0.4), 'BGR': (2.5, -2.5), 'BLR': (2.2, 1), 'CHE': (-0.3, -1.3), 'CZE': (0.5, -0.5), 'DEU': (0, 0), 'DNK': (0, 2), 'EST': (2, 2.5), 'ESP': (-1.5, -2), 'FIN': (2, 3.5), 'FRA': (-1, -1), 'GBR': (-2, 2.5), 'GRC': (1.3, -3.8), 'HRV': (0.8, -1.9), 'HUN': (1.5, -1), 'IRL': (-2.5, 2.5),
       'ITA': (0, -3), 'LTU': (2, 1.5), 'LUX': (-0.5, 0), 'LVA': (2, 2), 'MDA': (3, -1), 'MNE': (0.9, -2.8), 'MKD': (1.5, -3), 'MLT': (0, -3.8), 'NLD': (-0.5, 1), 'NOR': (0, 3.5), 'POL': (1.3, 0.2), 'PRT': (-2.5, -2), 'ROU': (2.5, -1), 'SRB': (1.5, -2.2), 'RUS': (3.7, 2.5), 'SWE': (1, 2.5), 'SVN': (0.6, -1.5), 'SVK': (1, -0.5), 'TUR': (3.5, -3.5), 'UKR': (3, 0.5)}

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

'''
here there is the function that fill the Matrix with the data
of the import-export of the electricity through the states.
'''


def FillMatrix():
    matrix = np.zeros((len(G.nodes), len(G.nodes)))
    df = pd.read_csv("Imp-Exp_2020.txt")
    for i in range(len(G.nodes)):
        for j in range(len(G.nodes)):
            if not df.loc[(df['source'] == Nations[i]) & (df['target'] == Nations[j])].empty:
                matrix[i][j] = df.loc[(df['source'] == Nations[i]) & (
                    df['target'] == Nations[j]), 'value'].iloc[0]
            else:
                pass

    return matrix


Matrix = FillMatrix()


'''
This function creates the links of the graph.
'''


def NetwokEdges():
    edges = []
    for i in range(len(G)):
        for j in range(len(G)):
            if i < j:
                if Matrix[i][j] != 0.0 or Matrix[j][i] != 0.0:
                    if Matrix[i][j]-Matrix[j][i] >= 0:
                        edges.append(
                            (Nations[i], Nations[j], (Matrix[i][j]-Matrix[j][i])))
                    else:
                        edges.append(
                            (Nations[j], Nations[i], (Matrix[j][i]-Matrix[i][j])))
                else:
                    pass
            else:
                pass

    return edges


Edges = NetwokEdges()
G.add_weighted_edges_from(Edges)


def LogDensity(graph):
    density = nx.density(graph)
    density = round(density, 4)
    print("Density of the graph:", density)


def Communities():
    partition = nx.community.greedy_modularity_communities(G, weight='weight')

    # Stampa l'assegnazione delle comunità per ogni nodo
    print("Communitites:")
    for community_id, community in enumerate(partition):
        for node in community:
            print(f"Nodo {node}: Comunità {community_id}")


'''
The next function use a built-in function of networkx called hits().
States with high value of hub have a great capacity to export electricity to other countries,
states with high value oh authority have a high dependance on the electricity imported
from other countries. 
'''


def hits():
    hubs, authorities = nx.hits(
        G, max_iter=100, tol=1e-15, nstart=None, normalized=True)
    hubs = sorted(hubs.items(), key=lambda x: x[1], reverse=True)
    authorities = sorted(authorities.items(), key=lambda x: x[1], reverse=True)

    hubs = [(node, round(value, 3)) for node, value in hubs]
    authorities = [(node, round(value, 3)) for node, value in authorities]

    return hubs, authorities


Hubs, Authorities = hits()

'''Print to terminal the results oh function hits'''


def Printhits():
    print("Hubs:")
    for node, value in Hubs:
        print(f"{node}: {value}")

    print("Authorities:")
    for node, value in Authorities:
        print(f"{node}: {value}")


edge_weights = [G[u][v]['weight']/400000 for u, v in G.edges()]

nx.draw(G, pos=pos, node_size=[
        x * 8 for x in TotalProduction2020], node_color=ColorMap, with_labels=True, font_size=8, width=edge_weights)

LogDensity(G)
Communities()
Printhits()
plt.show()
