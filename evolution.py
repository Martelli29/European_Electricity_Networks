import networkx as nx
import pandas as pd
import csv
import numpy as np
import draw as dr
import graph as gp


def GetNodes():
    '''
    This function gets the names of the nodes of the network
    from "Nations.txt" file and puts them in a list.

    This function returns a list with the names of the nodes.
    '''

    nations = []
    with open("DataSet/Nations.txt", "r") as file:
        next(file)  # skip first row
        row = next(file)  # second row
        nations = row.strip().split(",")  # get name of the nations from the file
    return nations


def GetTotalProduction():
    '''
    this function gets the values of the total electricity production (TWh)
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


def FillMatrix(Nations):
    '''
    This function creates an adjaceny matrix (nxn) where n is a number of the nodes
    of the network and fills it with the values of the electricity (W)
    using "Imp-Exp_2017-19.txt" file.

    This function needs one parameter:
    -Nations (list): name of the nodes/nations of the graph.

    This function returns a matrix in which each value x_ij represents
    the amount of electricity flowing from the i-th node to the j-th node.
    '''

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


def RealCarbonDensity(Nations, AdjMatrix, carbondensity, totalproduction):
    '''
    This function calculates total consumption and carbon density of each state that
    considers also the contributes of the electricity import-export.

    This function needs four parameters:
    -Nations (list): name of the nodes/nations of the graph.
    -AdjMatrix (matrix): adjacency matrix with the values of the flows x_ij between the nodes.
    -carbondensity (list): values of the carbon density of the states.
    -totalproduction (list): values of the energy production of the states.

    This function return two list that are the total consumption and the carbon
    density of the states also considering the electricity trades.
    '''

    totalconsumption = []
    realcarbondensity = []

    Num = []
    Den = []
    Cons = []

    for i in range(len(Nations)):
        num = 0
        den = 0
        cons = 0

        for j in range(len(Nations)):
            if AdjMatrix[i][j] != 0.0 or AdjMatrix[j][i] != 0.0:
                # 8760*10**-9 is W-TWh conversion
                num = num+AdjMatrix[j][i]*(8760*10**-9)*carbondensity[j]
                den = den+AdjMatrix[j][i]*(8760*10**-9)
                cons = cons-AdjMatrix[i][j] + AdjMatrix[j][i]
            else:
                pass
        else:
            pass

        Cons.append(cons)
        Num.append(num)
        Den.append(den)

        realcarbondensity.append(
            (totalproduction[i]*carbondensity[i]+Num[i])/(Den[i]+totalproduction[i]))
        totalconsumption.append(totalproduction[i]+(Cons[i]*(8760*10**-9)))

    return totalconsumption, realcarbondensity


def NetworkEdges(Nations, AdjMatrix):
    '''
    This function fills a list that networkx needs for the creation of the links
    for a weighted directed network.

    This function needs teo parameters:
    -Nations (list): name of the nodes/nations of the graph.
    -AdjMatrix (matrix): adjacency matrix with the values of the flows x_ij between the nodes.

    This function returns a list with the flux x_ij between states in a format that
    is accepted by NetworkX.
    '''

    edges = []
    for i in range(len(Nations)):
        for j in range(len(Nations)):
            if i < j:
                if AdjMatrix[i][j] != 0.0 or AdjMatrix[j][i] != 0.0:
                    if AdjMatrix[i][j]-AdjMatrix[j][i] >= 0:
                        edges.append(
                            (Nations[i], Nations[j], (AdjMatrix[i][j]-AdjMatrix[j][i])))
                    else:
                        edges.append(
                            (Nations[j], Nations[i], (AdjMatrix[j][i]-AdjMatrix[i][j])))
                else:
                    pass
            else:
                pass
    return edges


def Balancer(nodes, Balance, NewCons, pil, cc):
    '''
    Function that allow to redistribute the new imp-exp balance in such a way that each state
    don't import an amount of electricity greater than 5% of the own total consumption
    or don't export an amount of electricity than 15% of the own total consumption.

    This function need five parameters:
    -nodes (list): name of the nodes/nations of the graph.
    -Balance (list): difference between electricity consumption and electricity production of each state.
    -NewCons (list): energy consumption of each state in 2050.
    -pil (list): PIL of each state.
    -cc (list): closeness centrality for each state of a unweighted undirected network. 
    '''
    for i in range(len(nodes)):

        if Balance[i] < 0 and (abs(Balance[i])*(8760*10**-9)/NewCons[i] > 0.05):
            balance = 0.005*abs(Balance[i])
            Balance[i] = Balance[i]+0.005*abs(Balance[i])
            for j in range(len(nodes)):
                Balance[j] = Balance[j] - \
                    (balance*(pil[j]/sum(pil)+(cc[j]/sum(cc)))/2)
        else:
            pass
        if Balance[i] > 0 and (abs(Balance[i])*(8760*10**-9)/NewCons[i] > 0.15):
            balance = 0.015*abs(Balance[i])
            Balance[i] = Balance[i]-0.015*abs(Balance[i])
            for j in range(len(nodes)):
                Balance[j] = Balance[j] + \
                    (balance*(pil[j]/sum(pil)+(cc[j]/sum(cc)))/2)
        else:
            pass


def BalancerIterator(nodes, Balance, NewCons):
    '''
    This function is complementary to the function Balancer.
    Is used for reiterate the Balancer function until the condition that allow
    to import an amount of electricity smaller than 5% of the own total consumption or
    not greater than 15% of the own total consumption is satisfied.

    This function need three parameters:
    -nodes (list): name of the nodes/nations of the graph.
    -Balance (list): difference between electricity consumption and electricity production of each state.
    -NewCons (list): energy consumption of each state in 2050.
    '''
    for i in range(len(nodes)):
        if (Balance[i] < 0 and (abs(Balance[i])*(8760*10**-9)/NewCons[i] > 0.05)) or (Balance[i] > 0 and (abs(Balance[i])*(8760*10**-9)/NewCons[i] > 0.15)):
            return True
    return False


def Grid2050(nodes, totalconsumption, adjmatrix):
    '''
    This is a big function that does a lot of small different calculations.

    Initially the function takes the values of the electricity production of each state from
    fossil fuels (gas, coal and oil) and subtract them from the total consumption of each state.
    Then there is a creation of two list, first one is a prevision of the total consumption
    for each state in 2050 that has been hypothesized to be 40% greater.
    Second one is a calculation of a gap that each state have to be closed from the actual
    energy prouction without the fossil fuels and the future electricity consumption.

    To fill the missing power, a new criterion has been created. Each state have to contribute
    on the new power supply proportionally on the PIL and closeness centrality of a
    unweighted undirected network of the european electricity grid.
    The results of this calculation are subtracted by the gap of each state.
    The result is a list with the amount of electricity that each state have to
    import (negative value) or export (positive value), obviously the summation of all
    the import-export is equal to zero.

    The final part of the function is one of the two heaviest computational parts of this project,
    the functions Balancer(...) and IteratorBalancer(...) are called for obtain a more rational
    values of the import-export between states (a more helpfully description of this two 
    functions are in the declaration of them in the previous lines of this file).

    This function needs three parameters:
    -nodes (list): name of the nodes/nations of the graph.
    -totalconsumption (list): electricity consumption of each state.
    -adjmatrix (matrix): adjacency matrix with the values of the flows x_ij between the nodes.

    This function returns three list that are used in the following part of the code: first 
    one is the consumption of each state without the fossil fuels, second one is the
    consumption of each state in 2050, last one is the amount of electricity that each state
    have to import (negative value) or export (positive value).
    '''

    '''Fill a list with energy production without fossil fuels (FF).'''
    FFDeficit = []
    with open('DataSet/Electricity_Production_TWh_FINAL.txt', 'r') as file:
        TotalEnergy = csv.reader(file)
        next(TotalEnergy)   # skip first row
        for row in TotalEnergy:
            last_column = float(row[1])+float(row[2])+float(row[6])
            FFDeficit.append(last_column)
        FFDeficit = list(map(float, FFDeficit))

    '''Fill a list with the energy consumption without fossil fuels.'''
    ConsumptionWithoutFF = []
    for i in range(len(nodes)):
        ConsumptionWithoutFF.append(totalconsumption[i]-FFDeficit[i])

    '''List with a increase of energy consumption in 2050 of 40%.'''
    Consumption2050 = []
    for i in range(len(nodes)):
        Consumption2050.append(totalconsumption[i]+0.4*totalconsumption[i])

    '''Gap of energy supply that all countries have to fill'''
    Gap = []
    for i in range(len(nodes)):
        Gap.append(Consumption2050[i]-ConsumptionWithoutFF[i])

    '''
    Actual PIL of the states that will be used as a criterion for the allocation 
    of the new electricity supply.
    '''
    PIL = []
    with open("DataSet/Nations.txt", "r") as file:
        next(file)  # skip first row
        next(file)  # skip second row
        row = next(file)  # third row
        PIL = row.strip().split(",")
        PIL = list(map(float, PIL))

    '''
    Undirected unweighted graph created for the calculation of a closeness centrality
    used as a criterion for the allocation of the new electricity supply.
    '''
    ccG = nx.Graph()

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if adjmatrix[i][j] != 0.0 or adjmatrix[j][i] != 0.0:
                ccG.add_edge(nodes[i], nodes[j])
            else:
                pass

    cc = nx.closeness_centrality(ccG)
    cc = [cc[nation] for nation in nodes]

    '''List with the new power supply for each state.'''
    NewPower = []
    for i in range(len(nodes)):
        NewPower.append(sum(Gap)*(PIL[i]/sum(PIL)+(cc[i]/sum(cc)))/2)

    '''Calculation of the balance of the electricity that each state have to import or export.'''
    Balance = []
    for i in range(len(nodes)):
        Balance.append(NewPower[i]-Gap[i])
        Balance[i] = Balance[i]/(8760*10**-9)

    '''Functions called for a more rational values of the Balance of each state.'''
    while BalancerIterator(nodes, Balance, Consumption2050):
        Balancer(nodes, Balance, Consumption2050, PIL, cc)
        assert (sum(Balance) < 1*10**2 and sum(Balance) > -1*10**2)

    return ConsumptionWithoutFF, Consumption2050, Balance


'''Function that calculate values that will be assigned to new links of the network'''


def FlowsPropagator(nodes, newimpexp, matrix, matrix2050):
    for i in range(len(nodes)):
        if newimpexp[i] > 0.0:
            newimpexp[i] = newimpexp[i]-1*10**2
            non_zero_count = 0

            for count in range(len(nodes)):
                # state that need electricity
                if matrix[i][count] != 0 and newimpexp[count] < 1*10**2:
                    non_zero_count = non_zero_count+1
                else:
                    pass

            if non_zero_count != 0:
                for j in range(len(nodes)):
                    if matrix[i][j] != 0.0 and newimpexp[j] < 1*10**2:
                        newimpexp[j] = newimpexp[j]+(1*10**2/non_zero_count)
                        matrix2050[i][j] = matrix2050[i][j] + \
                            (1*10**2/non_zero_count)
                        matrix2050[j][i] = matrix2050[j][i] - \
                            (1*10**2/non_zero_count)
                    else:
                        pass

                assert (sum(newimpexp) < 1*10**2 and sum(newimpexp) > -1*10**2)

            elif non_zero_count == 0:
                for count in range(len(nodes)):
                    if matrix[i][count] != 0:
                        non_zero_count = non_zero_count+1
                    else:
                        pass

                for j in range(len(nodes)):
                    if matrix[i][j] != 0.0:
                        newimpexp[j] = newimpexp[j]+(1*10**2/non_zero_count)
                        matrix2050[i][j] = matrix2050[i][j] + \
                            (1*10**2/non_zero_count)
                        matrix2050[j][i] = matrix2050[j][i] - \
                            (1*10**2/non_zero_count)
                    else:
                        pass

                assert (sum(newimpexp) < 1*10**2 and sum(newimpexp) > -1*10**2)
        else:
            pass


'''iterator of the previous function'''


def IterFlowsPropagator(newimpexp):
    for i in newimpexp:
        if i >= 1*10**2:
            return True
    return False


def FillNewMatrix(nodes, balance, matrix, matrix2050):
    NewImpExp = []
    for i in range(len(nodes)):
        NewImpExp.append(balance[i])
    while IterFlowsPropagator(NewImpExp):
        FlowsPropagator(nodes, NewImpExp, matrix, matrix2050)


'''Function that create the links of the evoluted network using the value calculated from the previous function'''


def Edges2050(Nations, Matrix, Matrix2050):
    edges2050 = []
    for i in range(len(Nations)):
        for j in range(len(Nations)):
            if i < j:
                if Matrix[i][j] != 0.0 or Matrix[j][i] != 0.0:
                    if Matrix2050[i][j]-Matrix2050[j][i] >= 0:
                        edges2050.append(
                            (Nations[i], Nations[j], (Matrix2050[i][j])))
                    else:
                        edges2050.append(
                            (Nations[j], Nations[i], (Matrix2050[j][i])))
                else:
                    pass
            else:
                pass
    return edges2050


def LogResults(Nations, NewCons, Matrix2050):
    print("New consumption (TWh):")
    for i in range(len(Nations)):
        print(Nations[i], ":", NewCons[i])

    print("New electricity links (W):")
    for i in range(len(Nations)):
        for j in range(len(Nations)):
            if Matrix2050[i][j] != 0:
                print(Nations[i], "->", Nations[j], ":", Matrix2050[i][j])


'''This function calculate the contribute of the new power generated from solar/wind and nuclear '''


def NewCleanEnergy(nodes, NewCons, Balance, ConsWithoutFF):
    addnuclear = []
    addsolarwind = []
    SolarWind = []

    df = pd.read_csv("DataSet/Electricity_Production_TWh_FINAL.txt")
    for i in range(len(nodes)):
        SolarWind.append(float(df.iloc[i, 5])+float(df.iloc[i, 7]))

    solarwind = []
    for i in range(len(nodes)):
        solarwind.append(SolarWind[i])
        addsolarwind.append(0.0)
        addnuclear.append(0.0)

        # 50% of the electricity supply have to come from wind and sun
        while solarwind[i] <= 0.5*NewCons[i]+(Balance[i]*(8760*10**-9)):
            solarwind[i] = solarwind[i]+0.1  # useful only for the while cycle
            # 100 MW of new renewables added
            addsolarwind[i] = addsolarwind[i]+0.1

        # new consumption plus new solar/wind power, this variable will be used for the break condition of the next cycle
        provv = ConsWithoutFF[i]+addsolarwind[i]+(Balance[i]*(8760*10**-9))
        while provv < NewCons[i]:  # final gap that will be filled with new nuclear power
            provv = provv+0.1  # break condition
            addnuclear[i] = addnuclear[i]+0.1  # new nuclear power

    NewSolar = []
    NewWind = []
    NewNuclear = []
    for i in range(len(nodes)):
        NewSolar.append(addsolarwind[i]/1)
        NewWind.append(addsolarwind[i]/2.5)
        NewNuclear.append(addnuclear[i]/7.5)
        print(
            nodes[i], ":\n-Nuclear: {:.2f} TWh -> {:.2f} GW".format(addnuclear[i], NewNuclear[i]))
        print("-Renewables: {:.2f} TWh -> {:.2f}-{:.2f} GW".format(
            addsolarwind[i], NewWind[i], NewSolar[i]))

    return addsolarwind, addnuclear


'''
This function is used for the calculation of the carbon density of the states in 2050, it will be used 
for the creation of the nodes of the graph.
'''


def GetCarbonDensity2050(nodes, AddNuclear, AddSolarWind):
    Num = []
    Den = []
    IncrNum = []
    IncrDen = []
    carbonDensity2050 = []
    with open('DataSet/Electricity_Production_TWh_FINAL.txt', 'r') as file:
        f = csv.reader(file)
        next(f)   # skip first row
        for row in f:
            num = (float(row[3])*24+float(row[5])*44+float(row[7])*11+float(row[8])*12 +
                   float(row[4])*230)/(float(row[9])-float(row[1])-float(row[2])-float(row[6]))
            den = float(row[9])-float(row[1])-float(row[2])-float(row[6])
            Num.append(num)
            Den.append(den)
        for i in range(len(nodes)):
            incrnum = (AddNuclear[i]*12+AddSolarWind[i]
                       * 44)/(AddNuclear[i]+AddSolarWind[i])
            incrden = AddNuclear[i]+AddSolarWind[i]
            IncrNum.append(incrnum)
            IncrDen.append(incrden)
            carbonDensity2050.append(
                (Num[i]*Den[i]+IncrNum[i]*IncrDen[i])/(Den[i]+IncrDen[i]))
        carbonDensity2050 = list(map(float, carbonDensity2050))

    return carbonDensity2050


# '''
if __name__ == "__main__":

    Nodes = GetNodes()
    Matrix = FillMatrix(Nodes)

    TotalConsumption, RealCarbonDensity = RealCarbonDensity(
        Nodes, Matrix, GetCarbonDensity(), GetTotalProduction())

    ConsumptionWithoutFF, Consumption2050, Balance = Grid2050(
        Nodes, TotalConsumption, Matrix)

    Matrix2050 = np.zeros((len(Nodes), len(Nodes)))

    FillNewMatrix(Nodes, Balance, Matrix, Matrix2050)

    LogResults(Nodes, Consumption2050, Matrix2050)

    AddSolarWind, AddNuclear = NewCleanEnergy(
        Nodes, Consumption2050, Balance, ConsumptionWithoutFF)
    CarbonDensity2050 = GetCarbonDensity2050(Nodes, AddNuclear, AddSolarWind)

    G = gp.DGraph()
    G.LinksCreation(NetworkEdges(Nodes, Matrix))

    uG = gp.DGraph()
    uG.LinksCreation(Edges2050(Nodes, Matrix, Matrix2050))
    uG.LinkDensity()
    uG.Communities()
    uG.hits()

    dr.plot(G, TotalConsumption, dr.ColorMap(G, RealCarbonDensity))
    dr.plot(uG, Consumption2050, dr.ColorMap(uG, CarbonDensity2050))
# '''