import networkx as nx
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

Nations = []
TotalProduction2020 = []
CarbonDensity2020 = []

with open("Nations.txt", "r") as file:
    next(file)  # skip first row
    row = next(file)  # second row
    Nations = row.strip().split(",")

with open('ElectricityProductionTWhFINAL.txt', 'r') as file:
    TotalEnergy = csv.reader(file)
    next(TotalEnergy)   # skip first row
    for row in TotalEnergy:
        last_column = row[-1]  # select last column
        TotalProduction2020.append(last_column)
    TotalProduction2020 = list(map(float, TotalProduction2020))


a = sum(TotalProduction2020)
print(a)

with open("sharebysourceCarbonDensity.txt", "r") as file:
    contribute = csv.reader(file)
    next(file)  # skip first row
    for row in contribute:
        last_column = row[-1]  # select last column
        CarbonDensity2020.append(last_column)
    CarbonDensity2020 = list(map(float, CarbonDensity2020))

lista = []
for i in range(len(Nations)):
    t = CarbonDensity2020[i]*TotalProduction2020[i]
    lista.append(t)

pes = sum(lista)/a
print(pes)

G = nx.DiGraph()


def NodeConstruction():
    for i in range(len(Nations)):
        G.add_node(str(Nations[i]))


pos = {'ALB': (1.1, -3), 'AUT': (0.3, -1), 'BIH': (0.7, -2), 'BEL': (-0.8, 0.5), 'BGR': (2.5, -2.5), 'BLR': (2.2, 1), 'CHE': (-0.3, -1), 'CZE': (0.5, -0.5), 'DEU': (0, 0), 'DNK': (0, 2), 'EST': (2, 2.5), 'ESP': (-1.5, -2), 'FIN': (2, 3.5), 'FRA': (-1, -1), 'GBR': (-2, 2.5), 'GRC': (1.3, -3.6), 'HRV': (0.8, -1.5), 'HUN': (1.5, -1), 'IRL': (-2.5, 2.5),
       'ITA': (0, -2), 'LTU': (2, 1.5), 'LUX': (-0.5, 0), 'LVA': (2, 2), 'MDA': (3, -1), 'MNE': (0.9, -2.5), 'MKD': (1.5, -3), 'MLT': (0, -3), 'NLD': (-0.5, 1), 'NOR': (0, 3.5), 'POL': (1.3, 0.2), 'PRT': (-2.5, -2), 'ROU': (2.5, -1), 'SRB': (1.5, -2.2), 'RUS': (3.7, 2.5), 'SWE': (1, 2.5), 'SVN': (0.6, -1.2), 'SVK': (1, -0.5), 'TUR': (3.5, -3.5), 'UKR': (3, 0.5)}

NodeConstruction()


matrix = np.zeros((len(G.nodes), len(G.nodes)))


def FillMatrix():
    df = pd.read_csv("Imp-Exp_2017-19.txt")
    for i in range(len(G.nodes)):
        for j in range(len(G.nodes)):
            if not df.loc[(df['source'] == Nations[i]) & (df['target'] == Nations[j])].empty:
                matrix[i][j] = df.loc[(df['source'] == Nations[i]) & (
                    df['target'] == Nations[j]), 'value'].iloc[0]
            else:
                pass


FillMatrix()


TotalConsumption = []
RealCarbonDensity = []


def RCD():

    Num = []
    Den = []
    Cons = []

    for i in range(len(G)):
        num = 0
        den = 0
        cons = 0

        for j in range(len(G)):
            if matrix[i][j] != 0.0 or matrix[j][i] != 0.0:
                num = num+matrix[j][i]*(8760*10**-9)*CarbonDensity2020[j]
                den = den+matrix[j][i]*(8760*10**-9)
                cons = cons-matrix[i][j] + matrix[j][i]
            else:
                pass
        else:
            pass

        Cons.append(cons)
        Num.append(num)
        Den.append(den)

        RealCarbonDensity.append(
            (TotalProduction2020[i]*CarbonDensity2020[i]+Num[i])/(Den[i]+TotalProduction2020[i]))
        TotalConsumption.append(TotalProduction2020[i]+(Cons[i]*(8760*10**-9)))


RCD()


ColorMap = []
for i in range(len(G)):
    if RealCarbonDensity[i] < 100.0:
        ColorMap.append("green")
    elif RealCarbonDensity[i] >= 100 and RealCarbonDensity[i] < 200:
        ColorMap.append("lightgreen")
    elif RealCarbonDensity[i] >= 200 and RealCarbonDensity[i] < 300:
        ColorMap.append("yellow")
    elif RealCarbonDensity[i] >= 300 and RealCarbonDensity[i] < 400:
        ColorMap.append("orange")
    elif RealCarbonDensity[i] >= 400 and RealCarbonDensity[i] < 500:
        ColorMap.append("red")
    elif RealCarbonDensity[i] >= 500:
        ColorMap.append("brown")


Edges = []
for i in range(len(G)):
    for j in range(len(G)):
        if i < j:
            if matrix[i][j] != 0.0 or matrix[j][i] != 0.0:
                if matrix[i][j]-matrix[j][i] >= 0:
                    Edges.append(
                        (Nations[i], Nations[j], (matrix[i][j]-matrix[j][i])))
                else:
                    Edges.append(
                        (Nations[j], Nations[i], (matrix[j][i]-matrix[i][j])))
            else:
                pass
        else:
            pass

G.add_weighted_edges_from(Edges)
degree_dict = dict(G.degree(G.nodes()))


# bc = nx.betweenness_centrality(G, normalized=True, endpoints=True, weight='weight')
# print(bc) #non so se è utile

# closeness_centrality = nx.closeness_centrality(G, distance='weight', wf_improved=True)
# print(closeness_centrality) #non so se è utile

# hits = nx.hits(G, max_iter=100, tol=1e-15, nstart=None, normalized=True)
# print(hits)

def draw():
    edge_weights = [G[u][v]['weight']/400000 for u, v in G.edges()]

    nx.draw(G, pos=pos, node_size=[
        x * 8 for x in TotalConsumption], node_color=ColorMap, with_labels=True, font_size=8, width=edge_weights)

    plt.show()


draw()





CoalDeficit = []
with open('ElectricityProductionTWhFINAL.txt', 'r') as file:
    TotalEnergy = csv.reader(file)
    next(TotalEnergy)   # skip first row
    for row in TotalEnergy:
        last_column = row[-2]
        CoalDeficit.append(last_column)
    CoalDeficit = list(map(float, CoalDeficit))

ConsWithoutCoal = []
for i in range(len(Nations)):
    ConsWithoutCoal.append(TotalConsumption[i]-CoalDeficit[i])

NewCons = []
Gap = []
for i in range(len(Nations)):
    NewCons.append(TotalConsumption[i]+0.5*TotalConsumption[i])
    Gap.append(NewCons[i]-ConsWithoutCoal[i])

PIL = []
with open("Nations.txt", "r") as file:
    next(file)  # skip first row
    next(file)  # skip second row
    row = next(file)  # third row
    PIL = row.strip().split(",")
    PIL = list(map(float, PIL))

NewPower = []
for i in range(len(Nations)):
    NewPower.append(sum(Gap)*(PIL[i]/sum(PIL)))

NewImpExp = []
for i in range(len(Nations)):
    NewImpExp.append(NewPower[i]-Gap[i])
    NewImpExp[i] = NewImpExp[i]/(8760*10**-9)
    print(Nations[i], NewImpExp[i])
print(sum(NewImpExp))


def iterator(list):
    for i in list:
        if i >= 1*10**3:
            return False
    return True


'''
def magia():
    for i in range(len(G)):
        if NewImpExp[i] > 0.0:
            NewImpExp[i] = NewImpExp[i]-1*10**3
            non_zero_count = 0
            for count in range(len(G)):
                if matrix[i][count] != 0 and NewImpExp[count] < 1*10**3: # state that need electricity
                    non_zero_count = non_zero_count+1 
                else:
                    pass    
            if non_zero_count==0:
                for count in range(len(G)):
                    if matrix[i][count] != 0:
                        non_zero_count = non_zero_count+1
                    else:
                        pass    
            else:
                pass
            for j in range(len(G)):
                if non_zero_count == 0:
                    pass
                elif matrix[i][j] != 0.0 and NewImpExp[j] < 1*10**3:
                    NewImpExp[j] = NewImpExp[j]+(1*10**3/non_zero_count)
                else:
                    pass
        else:
            pass
'''

NewMatrix = np.zeros((len(Nations), len(Nations)))


def magia():
    for i in range(len(G)):
        if NewImpExp[i] > 0.0:
            NewImpExp[i] = NewImpExp[i]-1*10**3
            non_zero_count = 0

            for count in range(len(G)):
                # state that need electricity
                if matrix[i][count] != 0 and NewImpExp[count] < 1*10**3:
                    non_zero_count = non_zero_count+1
                else:
                    pass

            if non_zero_count != 0:
                for j in range(len(G)):
                    if matrix[i][j] != 0.0 and NewImpExp[j] < 1*10**3:
                        NewImpExp[j] = NewImpExp[j]+(1*10**3/non_zero_count)
                        NewMatrix[i][j] = NewMatrix[i][j] + (1*10**3/non_zero_count)
                        NewMatrix[j][i] = NewMatrix[j][i] - (1*10**3/non_zero_count)
                    else:
                        pass

                assert (sum(NewImpExp) < 1*10**3 or sum(NewImpExp) > -1*10**3)

            elif non_zero_count == 0:
                for count in range(len(G)):
                    if matrix[i][count] != 0:
                        non_zero_count = non_zero_count+1
                    else:
                        pass

                for j in range(len(G)):
                    if matrix[i][j] != 0.0:
                        NewImpExp[j] = NewImpExp[j]+(1*10**3/non_zero_count)
                        NewMatrix[i][j] = NewMatrix[i][j] + (1*10**3/non_zero_count)
                        NewMatrix[j][i] = NewMatrix[j][i] - (1*10**3/non_zero_count)
                    else:
                        pass

                assert (sum(NewImpExp) < 1*10**3 or sum(NewImpExp) > -1*10**3)
        else:
            pass


while not iterator(NewImpExp):
    magia()


NewEdges = []
for i in range(len(G)):
    for j in range(len(G)):
        if i < j:
            if matrix[i][j] != 0.0 or matrix[j][i] != 0.0:
                if NewMatrix[i][j]-NewMatrix[j][i] >= 0:
                    NewEdges.append(
                        (Nations[i], Nations[j], (NewMatrix[i][j])))
                else:
                    NewEdges.append(
                        (Nations[j], Nations[i], (NewMatrix[j][i])))
            else:
                pass
        else:
            pass

for i in range(len(G)):
    print(Nations[i], NewImpExp[i])
    for j in range(len(G)):
        if NewMatrix[i][j] != 0:
            print(Nations[i], Nations[j], NewMatrix[i][j])


uG = nx.DiGraph()

for i in range(len(Nations)):
    uG.add_node(str(Nations[i]))

uG.add_weighted_edges_from(NewEdges)


Newedge_weights = [uG[u][v]['weight']/1800000 for u, v in uG.edges()]

nx.draw(uG, pos=pos, node_size=[
    x * 8 for x in NewCons], node_color=ColorMap, with_labels=True, font_size=8, width=Newedge_weights)

plt.show()


'''
SolWinSupp=[]
for i in range(len(Nations)):
    if #pd.solare+pd.eolico>0.5*TotalConsumption:
        #add renew
    else:
        #add nuclear
'''

# degree fatto
# matrice al quadrato
# centralità di flusso, ho foto su cell
# centralità di intermediazione di flusso
# resistenza di flusso
# pagerank?
