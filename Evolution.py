import networkx as nx
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np


'''This function get the names of the nodes of the network'''


def GetName():
    nations = []
    with open("Nations.txt", "r") as file:
        next(file)  # skip first row
        row = next(file)  # second row
        nations = row.strip().split(",")  # get name of the nations from the file
    return nations


Nations = GetName()

TotalProduction = []
CarbonDensity = []

'''in this file we get the values of electricity production for each state'''
with open('Electricity_Production_TWh_FINAL.txt', 'r') as file:
    TotalEnergy = csv.reader(file)
    next(TotalEnergy)   # skip first row
    for row in TotalEnergy:
        last_column = row[-1]  # select last column
        TotalProduction.append(last_column)
    TotalProduction = list(map(float, TotalProduction))


a = sum(TotalProduction)
print(a)

'''in this file we get the values of the carbon intensity of the electricity generation for each state'''
with open("sharebysourceCarbonDensity.txt", "r") as file:
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
print(pes)


G = nx.DiGraph()  # inizialization oh the graph


def NodeConstruction():  # construction of the node with the name of the states
    for i in range(len(Nations)):
        G.add_node(str(Nations[i]))


'''setting of the position of the nodes in the graph'''
pos = {'ALB': (1.1, -3.1), 'AUT': (0.3, -1.3), 'BIH': (0.7, -2.5), 'BEL': (-0.9, 0.4), 'BGR': (2.5, -2.5), 'BLR': (2.2, 1), 'CHE': (-0.3, -1.3), 'CZE': (0.5, -0.5), 'DEU': (0, 0), 'DNK': (0, 2), 'EST': (2, 2.5), 'ESP': (-1.5, -2), 'FIN': (2, 3.5), 'FRA': (-1, -1), 'GBR': (-2, 2.5), 'GRC': (1.3, -3.8), 'HRV': (0.8, -1.9), 'HUN': (1.5, -1), 'IRL': (-2.5, 2.5),
       'ITA': (0, -3), 'LTU': (2, 1.5), 'LUX': (-0.5, 0), 'LVA': (2, 2), 'MDA': (3, -1), 'MNE': (0.9, -2.8), 'MKD': (1.5, -3), 'MLT': (0, -3.8), 'NLD': (-0.5, 1), 'NOR': (0, 3.5), 'POL': (1.3, 0.2), 'PRT': (-2.5, -2), 'ROU': (2.5, -1), 'SRB': (1.5, -2.2), 'RUS': (3.7, 2.5), 'SWE': (1, 2.5), 'SVN': (0.6, -1.5), 'SVK': (1, -0.5), 'TUR': (3.5, -3.5), 'UKR': (3, 0.5)}

NodeConstruction()

'''
here there is the function that fill the Matrix with the data
of the import-export of the electricity through the states.
'''


def FillMatrix():
    matrix = np.zeros((len(G.nodes), len(G.nodes)))
    df = pd.read_csv("Imp-Exp_2017-19.txt")
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
This function is used for calculate the total consumption and carbon density for each state
considering the contributes of the electricity import-export
'''


def RCD():
    totalconsumption = []
    realcarbondensity = []

    Num = []
    Den = []
    Cons = []

    for i in range(len(G)):
        num = 0
        den = 0
        cons = 0

        for j in range(len(G)):
            if Matrix[i][j] != 0.0 or Matrix[j][i] != 0.0:
                num = num+Matrix[j][i]*(8760*10**-9)*CarbonDensity[j]
                den = den+Matrix[j][i]*(8760*10**-9)
                cons = cons-Matrix[i][j] + Matrix[j][i]
            else:
                pass
        else:
            pass

        Cons.append(cons)
        Num.append(num)
        Den.append(den)

        realcarbondensity.append(
            (TotalProduction[i]*CarbonDensity[i]+Num[i])/(Den[i]+TotalProduction[i]))
        totalconsumption.append(TotalProduction[i]+(Cons[i]*(8760*10**-9)))

    return totalconsumption, realcarbondensity


TotalConsumption, RealCarbonDensity = RCD()

'''
This function is used for the color of the nodes in the visualization of the graph, colors represent
the carbon density of the electric generation.
'''


def NodeColor(list):
    colormap = []
    for i in range(len(G)):
        if list[i] < 100.0:
            colormap.append("green")
        elif list[i] >= 100 and list[i] < 200:
            colormap.append("lightgreen")
        elif list[i] >= 200 and list[i] < 300:
            colormap.append("yellow")
        elif list[i] >= 300 and list[i] < 400:
            colormap.append("orange")
        elif list[i] >= 400 and list[i] < 500:
            colormap.append("red")
        elif list[i] >= 500:
            colormap.append("brown")
    return colormap


ColorMap = NodeColor(RealCarbonDensity)

'''
This function creates the links of the graph.
'''

def NetworkEdges():
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


Edges = NetworkEdges()  # Used for the assignement of the links to the network
G.add_weighted_edges_from(Edges)


'''
Graph drawing function
'''


def draw():
    edge_weights = [G[u][v]['weight']/400000 for u, v in G.edges()]

    nx.draw(G, pos=pos, node_size=[
        x * 8 for x in TotalConsumption], node_color=ColorMap, with_labels=True, font_size=8, width=edge_weights)

    plt.show()


draw()

'''
Undirected unweighted graph created for the calculation of a closeness centrality
used on the following code
'''
bcG = nx.Graph()
bcMatrix = np.zeros((len(Nations), len(Nations)))

for i in range(len(G)):
    for j in range(len(G)):
        if Matrix[i][j] != 0.0 or Matrix[j][i] != 0.0:
            bcG.add_edge(Nations[i], Nations[j])
        else:
            pass

cc = nx.closeness_centrality(bcG)
cc = [cc[nation] for nation in Nations]

'''Creation of a list that has the coal production for each state that will be removed'''


def CoalDeficitCalculator():
    coaldeficit = []
    with open('Electricity_Production_TWh_FINAL.txt', 'r') as file:
        TotalEnergy = csv.reader(file)
        next(TotalEnergy)   # skip first row
        for row in TotalEnergy:
            last_column = float(row[1])+float(row[2])+float(row[6])
            coaldeficit.append(last_column)
        coaldeficit = list(map(float, coaldeficit))
    return coaldeficit


CoalDeficit = CoalDeficitCalculator()

'''Electricity consumption without the coal'''
ConsWithoutCoal = []
for i in range(len(Nations)):
    ConsWithoutCoal.append(TotalConsumption[i]-CoalDeficit[i])


'''
There is the creation of two list, first one is a prevision of the total consumption
for each state that in 2050 that has been hypothesized to be 40% greater.
Second list is a calculation of a gap that each state have to be closed from the actual
energy prouction without the coal and the future electricity consumption.
'''
NewCons = []
Gap = []
for i in range(len(Nations)):
    NewCons.append(TotalConsumption[i]+0.4*TotalConsumption[i])
    Gap.append(NewCons[i]-ConsWithoutCoal[i])

'''Actual PIL of the states that will be used as a criterion for the allocation of the new electricity supply.'''
PIL = []
with open("Nations.txt", "r") as file:
    next(file)  # skip first row
    next(file)  # skip second row
    row = next(file)  # third row
    PIL = row.strip().split(",")
    PIL = list(map(float, PIL))

'''Allocation for each state of the new power'''


def NewPowerFunction():
    newpower = []
    for i in range(len(Nations)):
        newpower.append(sum(Gap)*(PIL[i]/sum(PIL)+(cc[i]/sum(cc)))/2)
        print(Nations[i], PIL[i]/sum(PIL), cc[i]/sum(cc))
    return newpower


NewPower = NewPowerFunction()

'''Calculation of the balance of the electricity that each state has from the import-export'''
Balance = []
for i in range(len(Nations)):
    Balance.append(NewPower[i]-Gap[i])
    Balance[i] = Balance[i]/(8760*10**-9)
    print(Nations[i], Balance[i])
print(sum(Balance))

'''
Function that allow to reorganize the new imp-exp balance in sucha a way that each state
don't import an amount of electricity greater than 5% of the own total consumption.
'''


def calculator():
    for i in range(len(Nations)):

        if Balance[i] < 0 and (abs(Balance[i])*(8760*10**-9)/NewCons[i] > 0.05):
            balance = 0.005*abs(Balance[i])
            Balance[i] = Balance[i]+0.005*abs(Balance[i])
            for j in range(len(Nations)):
                Balance[j] = Balance[j] - \
                    (balance*(PIL[j]/sum(PIL)+(cc[j]/sum(cc)))/2)
        else:
            pass
        if Balance[i] > 0 and (abs(Balance[i])*(8760*10**-9)/NewCons[i] > 0.15):
            balance = 0.015*abs(Balance[i])
            Balance[i] = Balance[i]-0.015*abs(Balance[i])
            for j in range(len(Nations)):
                Balance[j] = Balance[j] + \
                    (balance*(PIL[j]/sum(PIL)+(cc[j]/sum(cc)))/2)
        else:
            pass


'''iterator of the previous function, this function run until the previous condition is satsfied.'''


def iterator2():
    for i in range(len(Nations)):
        if (Balance[i] < 0 and (abs(Balance[i])*(8760*10**-9)/NewCons[i] > 0.05)) or (Balance[i] > 0 and (abs(Balance[i])*(8760*10**-9)/NewCons[i] > 0.15)):
            return True
    return False


while iterator2():
    calculator()
    assert (sum(Balance) < 1*10**3 and sum(Balance) > -1*10**3)


for i in range(len(Nations)):
    print(Nations[i], Balance[i], Balance[i]*(8760*10**-9), NewCons[i])
print(sum(Balance))


'''Function that calculate values that will be assigned to new links of the network'''
NewMatrix = np.zeros((len(Nations), len(Nations)))

NewImpExp = []
for i in range(len(Nations)):
    NewImpExp.append(Balance[i])


def magia():
    for i in range(len(G)):
        if NewImpExp[i] > 0.0:
            NewImpExp[i] = NewImpExp[i]-1*10**3
            non_zero_count = 0

            for count in range(len(G)):
                # state that need electricity
                if Matrix[i][count] != 0 and NewImpExp[count] < 1*10**3:
                    non_zero_count = non_zero_count+1
                else:
                    pass

            if non_zero_count != 0:
                for j in range(len(G)):
                    if Matrix[i][j] != 0.0 and NewImpExp[j] < 1*10**3:
                        NewImpExp[j] = NewImpExp[j]+(1*10**3/non_zero_count)
                        NewMatrix[i][j] = NewMatrix[i][j] + \
                            (1*10**3/non_zero_count)
                        NewMatrix[j][i] = NewMatrix[j][i] - \
                            (1*10**3/non_zero_count)
                    else:
                        pass

                assert (sum(NewImpExp) < 1*10**3 and sum(NewImpExp) > -1*10**3)

            elif non_zero_count == 0:
                for count in range(len(G)):
                    if Matrix[i][count] != 0:
                        non_zero_count = non_zero_count+1
                    else:
                        pass

                for j in range(len(G)):
                    if Matrix[i][j] != 0.0:
                        NewImpExp[j] = NewImpExp[j]+(1*10**3/non_zero_count)
                        NewMatrix[i][j] = NewMatrix[i][j] + \
                            (1*10**3/non_zero_count)
                        NewMatrix[j][i] = NewMatrix[j][i] - \
                            (1*10**3/non_zero_count)
                    else:
                        pass

                assert (sum(NewImpExp) < 1*10**3 and sum(NewImpExp) > -1*10**3)
        else:
            pass


'''iterator of the previous function'''


def iterator(list):
    for i in list:
        if i >= 1*10**3:
            return True
    return False


while iterator(NewImpExp):
    magia()

'''Function that create the links of the evoluted network using the value calculated from the previous function'''
NewEdges = []
for i in range(len(Nations)):
    for j in range(len(Nations)):
        if i < j:
            if Matrix[i][j] != 0.0 or Matrix[j][i] != 0.0:
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

for i in range(len(Nations)):
    print(Nations[i], NewImpExp[i])
    for j in range(len(Nations)):
        if NewMatrix[i][j] != 0:
            print(Nations[i], Nations[j], NewMatrix[i][j])


NewSupply = []
for i in range(len(Nations)):
    NewSupply.append(Gap[i]+Balance[i]*(8760*10**-9))
    print(Nations[i], Gap[i], Balance[i], NewSupply[i])


'''This function calculate the contribute of the new power generated from solar/wind and nuclear '''


def NewCleanEnergy():
    addnuclear = []
    addsolarwind = []
    SolarWind = []

    df = pd.read_csv("Electricity_Production_TWh_FINAL.txt")
    for i in range(len(Nations)):
        SolarWind.append(float(df.iloc[i, 5])+float(df.iloc[i, 7]))

    solarwind = []
    for i in range(len(Nations)):
        solarwind.append(SolarWind[i])
        addsolarwind.append(0.0)
        addnuclear.append(0.0)

        # 50% of the electricity supply have to come from wind and sun
        while solarwind[i] <= 0.5*NewCons[i]+(Balance[i]*(8760*10**-9)):
            solarwind[i] = solarwind[i]+0.1  # useful only for the while cycle
            # 100 MW of new renewables added
            addsolarwind[i] = addsolarwind[i]+0.1

        # new consumption plus new solar/wind power, this variable will be used for the break condition of the next cycle
        provv = ConsWithoutCoal[i]+addsolarwind[i]+(Balance[i]*(8760*10**-9))
        while provv < NewCons[i]:  # final gap that will be filled with new nuclear power
            provv = provv+0.1  # break condition
            addnuclear[i] = addnuclear[i]+0.1  # new nuclear power
        print(Nations[i], addsolarwind[i], addnuclear[i])

    return addsolarwind, addnuclear


AddSolarWind, AddNuclear = NewCleanEnergy()

NewSolar = []
NewWind = []
NewNuclear = []
for i in range(len(Nations)):
    NewSolar.append(AddSolarWind[i]/1)
    NewWind.append(AddSolarWind[i]/2.5)
    NewNuclear.append(AddNuclear[i]/7.5)
    print(
        Nations[i], ":\n-Nuclear: {:.2f} TWh -> {:.2f} GW".format(AddNuclear[i], NewNuclear[i]))
    print("-Renewables: {:.2f} TWh -> {:.2f}-{:.2f} GW".format(
        AddSolarWind[i], NewWind[i], NewSolar[i]))


'''
This function is used for the calculation of the carbon density of the states in 2050, it will be used 
for the creation of the nodes of the graph.
'''


def GetCarbonDensity2050():
    Num = []
    Den = []
    IncrNum = []
    IncrDen = []
    carbonDensity2050 = []
    with open('Electricity_Production_TWh_FINAL.txt', 'r') as file:
        f = csv.reader(file)
        next(f)   # skip first row
        for row in f:
            num = (float(row[3])*24+float(row[5])*44+float(row[7])*11+float(row[8])*12 +
                   float(row[4])*230)/(float(row[9])-float(row[1])-float(row[2])-float(row[6]))
            den = float(row[9])-float(row[1])-float(row[2])-float(row[6])
            Num.append(num)
            Den.append(den)
        for i in range(len(Nations)):
            incrnum = (AddNuclear[i]*12+AddSolarWind[i]
                       * 44)/(AddNuclear[i]+AddSolarWind[i])
            incrden = AddNuclear[i]+AddSolarWind[i]
            IncrNum.append(incrnum)
            IncrDen.append(incrden)
            carbonDensity2050.append(
                (Num[i]*Den[i]+IncrNum[i]*IncrDen[i])/(Den[i]+IncrDen[i]))
        carbonDensity2050 = list(map(float, carbonDensity2050))

    return carbonDensity2050


CarbonDensity2050 = GetCarbonDensity2050()

'''Inizialization of the new graph'''
uG = nx.DiGraph()

for i in range(len(Nations)):
    uG.add_node(str(Nations[i]))

uG.add_weighted_edges_from(NewEdges)


Newedge_weights = [uG[u][v]['weight']/400000 for u, v in uG.edges()]

ColorMap = NodeColor(CarbonDensity2050)

nx.draw(uG, pos=pos, node_size=[
    x * 8 for x in NewCons], node_color=ColorMap, with_labels=True, font_size=8, width=Newedge_weights)

plt.show()