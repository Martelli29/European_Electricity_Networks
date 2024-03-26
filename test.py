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


def test_evo_GetTotalProduction(TotalProduction=evo.GetTotalProduction()):
    '''
    Test the correct length of the list created by the function GetTotalProduction().

    I expect to obtain a length equal to 39 (number of the nodes of the netowrk).
    '''

    assert len(TotalProduction)==39

def test_evo_GetCarbonDensity(GetCarbonDensity=evo.GetCarbonDensity()):
    '''
    Test the correct length of the list created by the function GetCarbonDensity().

    I expect to obtain a length equal to 39 (number of the nodes of the netowrk).
    '''

    assert len(GetCarbonDensity)==39

def test_LinksContribute_RealCarbonDensity():
    '''
    Test the correct values of the real carbon density created by the function LinksCoontribute(...).

    I expect to obtain the correct values of the carbon density that take into account the
    electricity import-export. 
    '''

    TestNodes=["a","b"]
    TestMat = np.array([[0, 10],
                       [20, 0]])
    TestCarbonDens=[10,20]
    TestTotalProd=[0.0000876,10]
    TotalCons, RealCarbonDens=evo.LinksContribute(TestNodes,TestMat,TestCarbonDens,TestTotalProd)
    for i in range(len(TestNodes)):
        TotalCons[i]=round(TotalCons[i],3)
        RealCarbonDens[i]=round(RealCarbonDens[i],3)

    assert RealCarbonDens[0]==15
    assert RealCarbonDens[1]==20

def test_LinksContribute_RealTotalProduction():
    '''
    Test the correct values of the total consumption created by the function LinksCoontribute(...).

    I expect to obtain the correct values of the total consumption that take into account the
    electricity import-export.
    '''
    
    TestNodes=["a","b"]
    TestMat = np.array([[0, 10],
                       [20, 0]])
    TestCarbonDens=[10,20]
    TestTotalProd=[0.0000876,0.1]
    TotalCons, RealCarbonDens=evo.LinksContribute(TestNodes,TestMat,TestCarbonDens,TestTotalProd)
    for i in range(len(TestNodes)):
        TotalCons[i]=round(TotalCons[i],10)
        RealCarbonDens[i]=round(RealCarbonDens[i],10)

    assert TotalCons[0]==2*TestTotalProd[0]


def test_evo_NetworkEdges():
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
    edges=evo.NetworkEdges(nodes, matrix)

    assert edges==ControlEdges

#def test_evo_Balancer():
