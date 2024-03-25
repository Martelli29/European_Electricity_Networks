import pandas as pd
import csv
import numpy as np
import draw as dr
import graph as gp

def GetTotalProduction():
    '''
    This function gets the values of the total electricity production (TWh)
    for each state from "Electricity_Production_TWh_FINAL.txt" and puts them in a list.

    This function returns a list with the electricity of the nodes.
    '''
    totalproduction = []
    with open('DataSet/Electricity_Production_TWh_FINAL.txt', 'r') as file:
        TotalEnergy = csv.reader(file)
        next(TotalEnergy)   # skip first row
        for row in TotalEnergy:
            last_column = row[-1]  # select last column
            totalproduction.append(last_column)
        totalproduction = list(map(float, totalproduction))
    return totalproduction


def GetCarbonDensity():
    '''
    This function gets the values of the electricity carbon density (gCO2/kWh)
    for each state from "sharebysourceCarbonDensity.txt" and put them in a list.

    This function returns a list with the electricity carbon density of the nodes. 
    '''
    carbondensity = []
    with open("DataSet/sharebysourceCarbonDensity.txt", "r") as file:
        contribute = csv.reader(file)
        next(file)  # skip first row
        for row in contribute:
            last_column = row[-1]  # select last column
            carbondensity.append(last_column)
        carbondensity = list(map(float, carbondensity))
    return carbondensity


def FillMatrix(nodes):
    '''
    This function creates an adjaceny matrix (nxn) where n is a number of the nodes
    of the network and fills it with the values of the electricity (W)
    using "Imp-Exp_2017-19.txt" file.

    This function needs one parameter:
    -nodes (list): name of the nodes/nations of the graph.

    This function returns a matrix in which each value x_ij represents
    the amount of electricity flowing from the i-th node to the j-th node.
    '''
    matrix = np.zeros((len(nodes), len(nodes)))
    df = pd.read_csv("DataSet/Imp-Exp_2017-19.txt")
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
    for a weighted undirected network.

    This function needs two parameters:
    -nodes (list): name of the nodes/nations of the graph.
    -AdjMatrix (matrix): adjacency matrix with the values of the flows x_ij between the nodes.

    This function returns a list with the flux x_ij between states in a format that
    is accepted by NetworkX and an integer that represent the total flux (W) among the
    nodes of the graph.
    '''
    total = 0
    edges = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i < j:
                if AdjMatrix[i][j] != 0.0 or AdjMatrix[j][i] != 0.0:
                    edges.append(
                        (nodes[i], nodes[j], (AdjMatrix[i][j]+AdjMatrix[j][i])))
                    total = total+AdjMatrix[i][j]+AdjMatrix[j][i]
                else:
                    pass
            else:
                pass

    return edges, total


def PrintTotalFlux(flux):
    '''
    This function print the total electricity flux between the nodes.

    This function needs one parameter:
    -flux (list): total flux of the graph.
    '''
    flux = round(flux, 1)

    print("Total flux of the graph:", flux, "(W)\n")


if __name__ == "__main__":

    Nations = gp.GetNames()
    Matrix = FillMatrix(Nations)
    Edges, TotalFlux = NetworkEdges(Nations, Matrix)
    PrintTotalFlux(TotalFlux)

    G = gp.UGraph()
    G.LinksCreation(Edges)
    G.LinkDensity()
    G.Centralities()
    G.Communities()
    dr.plot(G, GetTotalProduction(), dr.ColorMap(G, GetCarbonDensity()))
