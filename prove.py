import networkx as nx
import pandas as pd
import csv
Nations2020=[]
TotalProduction2020=[]
with open('Electricity_Production_TWh2020_FINAL.txt', 'r') as file:
    TotalEnergy = csv.reader(file)
    next(TotalEnergy)
    for row in TotalEnergy:
        last_column = row[-1]  # seleziona l'ultima colonna
        TotalProduction2020.append(last_column)

with open("Imp-Exp_2020.txt", "r") as file:
    Names= csv.reader(file)
    next(file) # salta la prima riga
    
    row = next(file) # stampa la seconda riga
    Nations2020.append(row)
    Nations2020=[x.split(",") for x in Nations2020]

print(Nations2020)
print(TotalProduction2020)

