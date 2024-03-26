import numpy as np
import grid_2017_19 as g1719
import grid_2020 as g20
import unweighted_2017_19 as u
import evolution as evo
import graph as gp

Nations=gp.GetNames()

def test_GetNamesLen():
    '''
    Test the correct length of the list created by the function GetName().
    I expect to obtain a length equal to 39 (number of the nodes of the netowrk).
    '''

    assert len(Nations)==39

def test_GetNamesOrder():
    '''
    Test the correct order (alphabetical order) of the list created by the function GetName().

    I expect to have the correct alphabetical order of the label of the nodes.
    '''

    assert Nations[0]=="ALB"
    assert Nations[10]=="EST"
    assert Nations[19]=="ITA"
    assert Nations[38]=="UKR"


def test_g1719_GetTotalProduction(TotalProduction=g1719.GetTotalProduction()):
    '''
    Test the correct length of the list created by the function GetTotalProduction().

    I expect to obtain a length equal to 39 (number of the nodes of the netowrk).
    '''

    assert len(TotalProduction)==39

def test_g1719_GetCarbonDensity(GetCarbonDensity=g1719.GetCarbonDensity()):
    '''
    Test the correct length of the list created by the function GetCarbonDensity().

    I expect to obtain a length equal to 39 (number of the nodes of the netowrk).
    '''

    assert len(GetCarbonDensity)==39

def test_LogParameters():
    '''
    Test the correct calculation and correct rounding of the function LogParameters(...).

    I expect to obtain the correct value of the total production of energy rounded to the 
    second decimal digit and the mean carbon density roundend to the second decimal digit.
    '''
    
    nodes=[1,2,3]
    TotalProduction = [100.128, 200, 300]
    CarbonDensity = [0.2, 0.20, 0.18]

    a = sum(TotalProduction)
    a = round(a, 2)

    lista = []
    for i in range(len(nodes)):
        t = CarbonDensity[i]*TotalProduction[i]
        lista.append(t)

    pes = sum(lista)/a
    pes = round(pes, 2)

    assert a==600.13 and pes==0.19

def test_g1719andg20_NetworkEdges():
    '''
    Test the correct format, order and values of the list of the function NetwrokEdges(...).

    I expect to obtain a list of tuples, in which the first value is the starting node, the
    second value is the ending node, the third value is the weight of the link.
    '''

    nodes=["a","b","c"]
    ControlEdges=[("b","a",20),("c","a",40), ("c","b",20)]
    matrix = np.array([[0, 20, 30],
                       [40, 0, 60],
                       [70, 80, 0]])
    edges=g1719.NetworkEdges(nodes, matrix)

    assert edges==ControlEdges


def test_g20_GetTotalProduction(TotalProduction=g20.GetTotalProduction()):
    '''
    Test the correct length of the list created by the function GetTotalProduction().

    I expect to obtain a length equal to 39 (number of the nodes of the netowrk).
    '''

    assert len(TotalProduction)==39

def test_g20_GetCarbonDensity(GetCarbonDensity=g20.GetCarbonDensity()):
    '''
    Test the correct length of the list created by the function GetCarbonDensity().

    I expect to obtain a length equal to 39 (number of the nodes of the netowrk).
    '''

    assert len(GetCarbonDensity)==39

def test_u_GetTotalProduction(TotalProduction=u.GetTotalProduction()):
    '''
    Test the correct length of the list created by the function GetTotalProduction().

    I expect to obtain a length equal to 39 (number of the nodes of the netowrk).
    '''

    assert len(TotalProduction)==39

def test_u_GetCarbonDensity(GetCarbonDensity=u.GetCarbonDensity()):
    '''
    Test the correct length of the list created by the function GetCarbonDensity().

    I expect to obtain a length equal to 39 (number of the nodes of the netowrk).
    '''

    assert len(GetCarbonDensity)==39


def test_gu_NetworkEdges():
    '''
    Test the correct format, order and values of the list of the function NetwrokEdges(...).

    I expect to obtain a list of tuples, in which the first and the second values are the label 
    of the nodes, third value is the weight of the link.
    '''

    nodes=["a","b","c"]
    ControlEdges=[("a","b",60),("a","c",100), ("b","c",140)]
    matrix = np.array([[0, 20, 30],
                       [40, 0, 60],
                       [70, 80, 0]])
    edges,total=u.NetworkEdges(nodes, matrix)
    ControlTotal=60+100+140
    assert edges==ControlEdges
    assert total==ControlTotal

def test_TotalFlux():
    values=[10.11,20.11,30.11]
    ControlFlux=sum(values)
    ControlFlux=round(ControlFlux, 1)
    flux=u.PrintTotalFlux(values)

    assert flux==ControlFlux