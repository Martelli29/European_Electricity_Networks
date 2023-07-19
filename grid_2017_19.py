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

a = sum(TotalProduction)
a = round(a, 2)
print("Total production is:", a)

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

pes = sum(lista)/a
pes = round(pes, 2)
print("Mean carbon density is:", pes)

G = nx.DiGraph()  # inizialization of the graph


def NodeConstruction():  # construction of the node with the name of the states
    for i in range(len(Nations)):
        G.add_node(str(Nations[i]))


NodeConstruction()


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


Communities()


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



LogDensity(G)
Printhits()