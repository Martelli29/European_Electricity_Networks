import networkx as nx
import pandas as pd
import csv
Nations=[]
TotalProduction=[]
with open('Electricity_Production_TWh2020_FINAL.txt', 'r') as file:
    TotalEnergy = csv.reader(file)
    next(TotalEnergy)
    for row in TotalEnergy:
        last_column = row[-1]  # seleziona l'ultima colonna
        TotalProduction.append(last_column)

with open("Imp-Exp_2020.txt", "r") as file:
    Names= csv.reader(file)
    next(file) # salta la prima riga
    
    row = next(file) # stampa la seconda riga
    Nations.append(row)
    Nations=[x.split(",") for x in Nations]
print(Nations)
print(TotalProduction)

