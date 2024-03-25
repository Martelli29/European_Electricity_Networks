import pandas as pd
import csv
import numpy as np
import draw as dr
import graph as gp

def GetTotalProduction():
    '''
    This function gets the values of the total electricity production (TWh)
    for each state from "Electricity_Production_TWh2020_FINAL.txt" and puts them in a list.

    This function returns a list with the electricity of the nodes.
    '''
    totalproduction = []
    with open('DataSet/Electricity_Production_TWh2020_FINAL.txt', 'r') as file:
        TotalEnergy = csv.reader(file)
        next(TotalEnergy)
        for row in TotalEnergy:
            last_column = row[-1]  # seleziona l'ultima colonna
            totalproduction.append(last_column)
        totalproduction = list(map(float, totalproduction))
    return totalproduction


def GetCarbonDensity():
    '''
    This function gets the values of the electricity carbon density (gCO2/kWh)
    for each state from "share-by-source2020+Carbon_Density.txt" and put them in a list.

    This function returns a list with the electricity carbon density of the nodes. 
    '''
    carbondensity = []
    with open("DataSet/share-by-source2020+Carbon_Density.txt", "r") as file:
        contribute = csv.reader(file)
        next(file)  # skip first row
        for row in contribute:
            last_column = row[-1]  # seleziona l'ultima colonna
            carbondensity.append(last_column)
        carbondensity = list(map(float, carbondensity))
    return carbondensity


def GeneralParameters(nodes, TotalProduction, CarbonDensity):
    '''
    This function prints to the terminal the values of the total electricity
    production (TWh) and mean carbon density (gCO2/kWh).

    This function needs three parameters:
    -nodes (list): name of the nodes/nations of the graph.
    -TotalProduction (list): values of the energy production of the states.
    -CarbonDensity (list): values of the carbon density of the states.
    '''
    a = sum(TotalProduction)
    a = round(a, 2)
    print("Total production is:", a, "TWh\n")

    lista = []
    for i in range(len(nodes)):
        t = CarbonDensity[i]*TotalProduction[i]
        lista.append(t)

    pes = sum(lista)/a
    pes = round(pes, 2)
    print("Mean carbon density is:", pes, "gCO2/kWh\n")


def FillMatrix(nodes):
    '''
    This function creates an adjaceny matrix (nxn) where n is a number of the nodes
    of the network and fills it with the values of the electricity (W)
    using "Imp-Exp_2020.txt" file.

    This function needs one parameter:
    -nodes (list): name of the nodes/nations of the graph.

    This function returns a matrix in which each value x_ij represents
    the amount of electricity flowing from the i-th node to the j-th node.
    '''

    matrix = np.zeros((len(nodes), len(nodes)))
    df = pd.read_csv("DataSet/Imp-Exp_2020.txt")
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if not df.loc[(df['source'] == nodes[i]) & (df['target'] == nodes[j])].empty:
                matrix[i][j] = df.loc[(df['source'] == nodes[i]) & (
                    df['target'] == nodes[j]), 'value'].iloc[0]
            else:
                pass

    return matrix


def NetworkEdges(nodes, AdjMatrix):
    '''
    This function fills a list that networkx needs for the creation of the links
    for a weighted directed network.

    This function needs two parameters:
    -nodes (list): name of the nodes/nations of the graph.
    -AdjMatrix (matrix): adjacency matrix with the values of the flows x_ij between the nodes.

    This function returns a list with the flux x_ij between states in a format that
    is accepted by NetworkX.
    '''
    edges = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i < j:
                if AdjMatrix[i][j] != 0.0 or AdjMatrix[j][i] != 0.0:
                    if AdjMatrix[i][j]-AdjMatrix[j][i] >= 0:
                        edges.append(
                            (nodes[i], nodes[j], (AdjMatrix[i][j]-AdjMatrix[j][i])))
                    else:
                        edges.append(
                            (nodes[j], nodes[i], (AdjMatrix[j][i]-AdjMatrix[i][j])))
                else:
                    pass
            else:
                pass

    return edges


if __name__ == "__main__":
    Nations = gp.GetNames()
    Matrix = FillMatrix(Nations)

    GeneralParameters(Nations, GetTotalProduction(), GetCarbonDensity())

    # Creation of the graph declared in file graph.py.
    G = gp.DGraph()

    # Creation of the links of the graphs.
    G.LinksCreation(NetworkEdges(Nations, Matrix))

    G.LinkDensity()
    G.Communities()
    G.hits()

    # Plot of the graph (view graph.py file).
    dr.plot(G, GetTotalProduction(), dr.ColorMap(G, GetCarbonDensity()))
