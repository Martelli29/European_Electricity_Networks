import networkx as nx
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np


TotalProduction = []
CarbonDensity = []


'''This function get the names of the nodes of the network'''


def GetName():
    nations = []
    with open("DataSet/Nations.txt", "r") as file:
        next(file)  # skip first row
        row = next(file)  # second row
        nations = row.strip().split(",")  # get name of the nations from the file
    return nations


Nations = GetName()

'''in this file we get the values of electricity production for each state'''
with open('DataSet/Electricity_Production_TWh_FINAL.txt', 'r') as file:
    TotalEnergy = csv.reader(file)
    next(TotalEnergy)   # skip first row
    for row in TotalEnergy:
        last_column = row[-1]  # select last column
        TotalProduction.append(last_column)
    TotalProduction = list(map(float, TotalProduction))


'''in this file we get the values of the carbon intensity of the electricity generation for each state'''
with open("DataSet/sharebysourceCarbonDensity.txt", "r") as file:
    contribute = csv.reader(file)
    next(file)  # skip first row
    for row in contribute:
        last_column = row[-1]  # select last column
        CarbonDensity.append(last_column)
    CarbonDensity = list(map(float, CarbonDensity))

lista = []
for i in range(len(Nations)):
    t = CarbonDensity[i]*TotalProduction[i]
    lista.append(t)


G = nx.Graph()  # inizialization of the graph


def NodeConstruction():  # construction of the node with the name of the states
    for i in range(len(Nations)):
        G.add_node(str(Nations[i]))


pos = {'ALB': (1.1, -3.1), 'AUT': (0.3, -1.3), 'BIH': (0.7, -2.5), 'BEL': (-0.9, 0.4), 'BGR': (2.5, -2.5), 'BLR': (2.2, 1), 'CHE': (-0.3, -1.3), 'CZE': (0.5, -0.5), 'DEU': (0, 0), 'DNK': (0, 2), 'EST': (2, 2.5), 'ESP': (-1.5, -2), 'FIN': (2, 3.5), 'FRA': (-1, -1), 'GBR': (-2, 2.5), 'GRC': (1.3, -3.8), 'HRV': (0.8, -1.9), 'HUN': (1.5, -1), 'IRL': (-2.5, 2.5),
       'ITA': (0, -3), 'LTU': (2, 1.5), 'LUX': (-0.5, 0), 'LVA': (2, 2), 'MDA': (3, -1), 'MNE': (0.9, -2.8), 'MKD': (1.5, -3), 'MLT': (0, -3.8), 'NLD': (-0.5, 1), 'NOR': (0, 3.5), 'POL': (1.3, 0.2), 'PRT': (-2.5, -2), 'ROU': (2.5, -1), 'SRB': (1.5, -2.2), 'RUS': (3.7, 2.5), 'SWE': (1, 2.5), 'SVN': (0.6, -1.5), 'SVK': (1, -0.5), 'TUR': (3.5, -3.5), 'UKR': (3, 0.5)}

NodeConstruction()

ColorMap = []
for i in range(len(G)):
    if CarbonDensity[i] < 100.0:
        ColorMap.append("green")
    elif CarbonDensity[i] >= 100 and CarbonDensity[i] < 200:
        ColorMap.append("lightgreen")
    elif CarbonDensity[i] >= 200 and CarbonDensity[i] < 300:
        ColorMap.append("yellow")
    elif CarbonDensity[i] >= 300 and CarbonDensity[i] < 400:
        ColorMap.append("orange")
    elif CarbonDensity[i] >= 400 and CarbonDensity[i] < 500:
        ColorMap.append("red")
    elif CarbonDensity[i] >= 500:
        ColorMap.append("brown")

'''
here there is the function that fill the Matrix with the data
of the import-export of the electricity through the states.
'''


def FillMatrix():
    matrix = np.zeros((len(G.nodes), len(G.nodes)))
    df = pd.read_csv("DataSet/Imp-Exp_2017-19.txt")
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


def NetworkEdges():
    total = 0
    edges = []
    for i in range(len(G)):
        for j in range(len(G)):
            if i < j:
                if Matrix[i][j] != 0.0 or Matrix[j][i] != 0.0:
                    edges.append(
                        (Nations[i], Nations[j], (Matrix[i][j]+Matrix[j][i])))
                    total = total+Matrix[i][j]+Matrix[j][i]
                else:
                    pass
            else:
                pass

    return edges, total


Edges, Total = NetworkEdges()
G.add_weighted_edges_from(Edges)
Total = round(Total, 1)

print("Total flux of the graph:", Total)


def LogDensity(graph):
    density = nx.density(graph)
    density = round(density, 4)
    print("Density of the graph:", density)


LogDensity(G)


def Communities():
    partition = nx.community.greedy_modularity_communities(G, weight='weight')

    # Stampa l'assegnazione delle comunità per ogni nodo
    print("Communitites:")
    for community_id, community in enumerate(partition):
        for node in community:
            print(f"Nodo {node}: Comunità {community_id}")


edge_weights = [G[u][v]['weight']/400000 for u, v in G.edges()]

Communities()


def centralities():
    currentflow = nx.current_flow_betweenness_centrality(G, weight='weight')
    currentflow = sorted(currentflow.items(), key=lambda x: x[1], reverse=True)
    print("Current flow betweenness centrality:")
    for node, centrality in currentflow:
        centrality = round(centrality, 3)
        print(f"{node}: {centrality}")

    edgecurrentflow = nx.edge_current_flow_betweenness_centrality(
        G, weight='weight')
    edgecurrentflow = sorted(edgecurrentflow.items(),
                             key=lambda x: x[1], reverse=True)
    print("Edge current flow betweenness centrality:")
    for edge, centrality in edgecurrentflow:
        centrality = round(centrality, 3)
        print(f"{edge}: {centrality}")

    currentflowcloseness = nx.current_flow_closeness_centrality(
        G, weight='weight')
    currentflowcloseness = sorted(
        currentflowcloseness.items(), key=lambda x: x[1], reverse=True)
    print("Current flow closeness centrality:")
    for node, centrality in currentflowcloseness:
        centrality = round(centrality, 3)
        print(f"{node}: {centrality}")

    laplacian = nx.laplacian_centrality(G, weight='weight')
    laplacian = sorted(laplacian.items(), key=lambda x: x[1], reverse=True)
    print("Laplacian centrality:")
    for node, centrality in laplacian:
        centrality = round(centrality, 3)
        print(f"{node}: {centrality}")


centralities()

nx.draw(G, pos=pos, node_size=[
        x * 8 for x in TotalProduction], node_color=ColorMap, with_labels=True, font_size=8, width=edge_weights)


plt.show()
