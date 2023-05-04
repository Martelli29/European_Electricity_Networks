import networkx as nx
import pandas as pd
import csv
import matplotlib.pyplot as plt

Nations2020 = []
TotalProduction2020 = []
CarbonDensity2020 = []

with open("Imp-Exp_2020.txt", "r") as file:
    next(file)  # salta la prima riga
    row = next(file)  # stampa la seconda riga
    Nations2020 = row.strip().split(",")

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

for i in range(len(Nations2020)):
    G.add_node(str(Nations2020[i]))


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


nx.draw(G, node_size=[x * 20 for x in TotalProduction2020], node_color=ColorMap, with_labels=True)
plt.show()
