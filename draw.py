import networkx as nx
import matplotlib.pyplot as plt

'''setting of the position of the nodes in the graph'''
pos = {'ALB': (1.1, -3.1), 'AUT': (0.3, -1.3), 'BIH': (0.7, -2.5), 'BEL': (-0.9, 0.4), 'BGR': (2.5, -2.5), 'BLR': (2.2, 1), 'CHE': (-0.3, -1.3), 'CZE': (0.5, -0.5), 'DEU': (0, 0), 'DNK': (0, 2), 'EST': (2, 2.5), 'ESP': (-1.5, -2), 'FIN': (2, 3.5), 'FRA': (-1, -1), 'GBR': (-2, 2.5), 'GRC': (1.3, -3.8), 'HRV': (0.8, -1.9), 'HUN': (1.5, -1), 'IRL': (-2.5, 2.5),
       'ITA': (0, -3), 'LTU': (2, 1.5), 'LUX': (-0.5, 0), 'LVA': (2, 2), 'MDA': (3, -1), 'MNE': (0.9, -2.8), 'MKD': (1.5, -3), 'MLT': (0, -3.8), 'NLD': (-0.5, 1), 'NOR': (0, 3.5), 'POL': (1.3, 0.2), 'PRT': (-2.5, -2), 'ROU': (2.5, -1), 'SRB': (1.5, -2.2), 'RUS': (3.7, 2.5), 'SWE': (1, 2.5), 'SVN': (0.6, -1.5), 'SVK': (1, -0.5), 'TUR': (3.5, -3.5), 'UKR': (3, 0.5)}


def ColorMap(graph, carbondensity):
    colormap = []
    for i in range(len(graph)):
        if carbondensity[i] < 100.0:
            colormap.append("green")
        elif carbondensity[i] >= 100 and carbondensity[i] < 200:
            colormap.append("lightgreen")
        elif carbondensity[i] >= 200 and carbondensity[i] < 300:
            colormap.append("yellow")
        elif carbondensity[i] >= 300 and carbondensity[i] < 400:
            colormap.append("orange")
        elif carbondensity[i] >= 400 and carbondensity[i] < 500:
            colormap.append("red")
        elif carbondensity[i] >= 500:
            colormap.append("brown")
    return colormap


def plot(graph_class, production, colormap):
    edge_weights = graph_class.get_weights()

    nx.draw(graph_class.graph, pos=pos, node_size=[
            x * 8 for x in production], node_color=colormap, with_labels=True, font_size=8, width=edge_weights)

    plt.show()