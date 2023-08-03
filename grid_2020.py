import networkx as nx
import pandas as pd
import csv
import numpy as np
import draw as dr
import graph as gp





'''This function get the names of the nodes of the network'''


def GetName():
    nations = []
    with open("DataSet/Nations.txt", "r") as file:
        next(file)  # skip first row
        row = next(file)  # second row
        nations = row.strip().split(",")  # get name of the nations from the file
    return nations




'''in this file we get the values of electricity production for each state'''
def GetTotalProduction():
    totalproduction=[]
    with open('DataSet/Electricity_Production_TWh2020_FINAL.txt', 'r') as file:
        TotalEnergy = csv.reader(file)
        next(TotalEnergy)
        for row in TotalEnergy:
            last_column = row[-1]  # seleziona l'ultima colonna
            totalproduction.append(last_column)
        totalproduction = list(map(float, totalproduction))
    return totalproduction



'''in this file we get the values of the carbon intensity of the electricity generation for each state'''
def GetCarbonDensity():
    carbondensity=[]
    with open("DataSet/share-by-source2020+Carbon_Density.txt", "r") as file:
        contribute = csv.reader(file)
        next(file)  # skip first row
        for row in contribute:
            last_column = row[-1]  # seleziona l'ultima colonna
            carbondensity.append(last_column)
        carbondensity = list(map(float, carbondensity))
    return carbondensity

def GeneralParameters(Nations, TotalProduction, CarbonDensity):
    a = sum(TotalProduction)
    a = round(a, 2)
    print("Total production is:", a,"TWh\n")

    lista = []
    for i in range(len(Nations)):
        t = CarbonDensity[i]*TotalProduction[i]
        lista.append(t)

    pes = sum(lista)/a
    pes = round(pes, 2)
    print("Mean carbon density is:", pes, "gCO2/kWh\n")
'''
here there is the function that fill the Matrix with the data
of the import-export of the electricity through the states.
'''


def FillMatrix(nations):
    matrix = np.zeros((len(nations), len(nations)))
    df = pd.read_csv("DataSet/Imp-Exp_2020.txt")
    for i in range(len(nations)):
        for j in range(len(nations)):
            if not df.loc[(df['source'] == nations[i]) & (df['target'] == nations[j])].empty:
                matrix[i][j] = df.loc[(df['source'] == Nations[i]) & (
                    df['target'] == nations[j]), 'value'].iloc[0]
            else:
                pass

    return matrix





'''
This function creates the links of the graph.
'''


def NetworkEdges(nations, AdjMatrix):
    edges = []
    for i in range(len(nations)):
        for j in range(len(nations)):
            if i < j:
                if AdjMatrix[i][j] != 0.0 or AdjMatrix[j][i] != 0.0:
                    if AdjMatrix[i][j]-AdjMatrix[j][i] >= 0:
                        edges.append(
                            (nations[i], nations[j], (AdjMatrix[i][j]-AdjMatrix[j][i])))
                    else:
                        edges.append(
                            (nations[j], nations[i], (AdjMatrix[j][i]-AdjMatrix[i][j])))
                else:
                    pass
            else:
                pass

    return edges


'''
The next function use a built-in function of networkx called hits().
States with high value of hub have a great capacity to export electricity to other countries,
states with high value oh authority have a high dependance on the electricity imported
from other countries. 
'''

if __name__=="__main__":
    Nations = GetName()
    TotalProduction = GetTotalProduction()
    CarbonDensity = GetCarbonDensity()
    Matrix = FillMatrix(Nations)

    GeneralParameters(Nations, TotalProduction, CarbonDensity)

    G = gp.DGraph()
    G.LinksCreation(NetworkEdges(Nations, Matrix))
    G.LinkDensity()
    G.Communities()
    G.hits()

    dr.plot(G, TotalProduction, dr.ColorMap(G, CarbonDensity))