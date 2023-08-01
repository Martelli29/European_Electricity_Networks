import networkx as nx
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import graph as gp

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

G=gp.DGraph()



'''
here there is the function that fill the Matrix with the data
of the import-export of the electricity through the states.
'''


def FillMatrix():
    matrix = np.zeros((len(Nations), len(Nations)))
    df = pd.read_csv("DataSet/Imp-Exp_2017-19.txt")
    for i in range(len(Nations)):
        for j in range(len(Nations)):
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
    for i in range(len(Nations)):
        for j in range(len(Nations)):
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



G.LinksCreation(NetwokEdges())
G.LinkDensity()
G.Communities()
G.hits()



'''
The next function use a built-in function of networkx called hits().
States with high value of hub have a great capacity to export electricity to other countries,
states with high value oh authority have a high dependance on the electricity imported
from other countries. 
'''

