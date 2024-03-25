'''
In this file there are the definitions of the classes that are used in the simulations of this project.
'''

import networkx as nx


def GetNames():
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


class DGraph:
    def __init__(self):
        '''
        This is the constructor of the DGraph class. Within this constructor,
        the creation of the directed graph takes place using the NetworkX function "DiGraph()".
        Nodes are incorporated into the initially empty graph using the "add_node()" feature.
        A list of strings containing the country names is provided as an argument, which
        in turn assigns these names to the nodes.
        '''
        self.graph = nx.DiGraph()
        Nations = GetNames()
        for i in range(len(Nations)):
            self.graph.add_node(str(Nations[i]))

    def __len__(self):
        '''
        This function assigns the graph's length to the `DGraph` class.
        This length corresponds to the number of nodes present in the graph.
        '''
        return len(self.graph)

    def LinksCreation(self, WeightList):
        '''
        This function gives the weights of the links thanks to the
        "add_weighted_edges_from()" feature. A list of doubles, containing 
        the values of the weights, are provided as an argument.
        '''
        self.graph.add_weighted_edges_from(WeightList)

    def GetWeights(self):
        '''
        This function returns a list that provide the weights of the links to the
        drawing part of the program.
        '''
        return [self.graph[u][v]['weight']/400000 for u, v in self.graph.edges()]

    def LinkDensity(self):
        '''
        This function print the link density of the graph using the
        the NetworkX function called "density()" (more information in README.md).
        '''
        density = nx.density(self.graph)
        density = round(density, 4)
        print("Density of the graph:", density, "\n")

    def Communities(self):
        '''
        This function print the communities of the graph using the NetworkX function
        called "greedy_modularity_communities()" (more information in README.md).
        '''
        partition = nx.community.greedy_modularity_communities(
            self.graph, weight='weight')

        # Stampa l'assegnazione delle comunità per ogni nodo
        print("Communitites:")
        for community_id, community in enumerate(partition):
            for node in community:
                print(f"Nodo {node}: Comunità {community_id}")
        print()

    def hits(self):
        '''
        This function print the HITS (hubs and authorities) of each node of the graph
        using the NetworkX function called "hits()" (more information in README.md).
        '''
        hubs, authorities = nx.hits(
            self.graph, max_iter=100, tol=1e-15, nstart=None, normalized=True)
        hubs = sorted(hubs.items(), key=lambda x: x[1], reverse=True)
        authorities = sorted(authorities.items(),
                             key=lambda x: x[1], reverse=True)

        hubs = [(node, round(value, 3)) for node, value in hubs]
        authorities = [(node, round(value, 3)) for node, value in authorities]

        print("Hubs:")
        for node, value in hubs:
            print(f"{node}: {value}")

        print("Authorities:")
        for node, value in authorities:
            print(f"{node}: {value}")
        print()


class UGraph:
    def __init__(self):
        '''
        This is the constructor of the UGraph class. Within this constructor,
        the creation of the undirected graph takes place using the NetworkX function "Graph()".
        Nodes are incorporated into the initially empty graph using the "add_node()" feature.
        A list of strings containing the country names is provided as an argument, which
        in turn assigns these names to the nodes.
        '''
        self.graph = nx.Graph()
        Nations = GetNames()
        for i in range(len(Nations)):
            self.graph.add_node(str(Nations[i]))

    def __len__(self):
        '''
        This function assigns the graph's length to the DGraph class.
        This length corresponds to the number of nodes present in the graph.
        '''
        return len(self.graph)

    def LinksCreation(self, WeightList):
        '''
        This function gives the weights of the links thanks to the
        "add_weighted_edges_from()" feature. A list of doubles, containing 
        the values of the weights, are provided as an argument.
        '''
        self.graph.add_weighted_edges_from(WeightList)

    def GetWeights(self):
        '''
        This function returns a list that provide the weights of the links to the
        drawing part of the program.
        '''
        return [self.graph[u][v]['weight']/400000 for u, v in self.graph.edges()]

    def LinkDensity(self):
        '''
        This function print the link density of the graph using the
        the NetworkX function called "density()" (more information in README.md).
        '''
        density = nx.density(self.graph)
        density = round(density, 4)
        print("Density of the graph:", density, "\n")

    def Communities(self):
        '''
        This function print the communities of the graph using the NetworkX function
        called "greedy_modularity_communities()" (more information in README.md).
        '''
        partition = nx.community.greedy_modularity_communities(
            self.graph, weight='weight')

        # Stampa l'assegnazione delle comunità per ogni nodo
        print("Communitites:")
        for community_id, community in enumerate(partition):
            for node in community:
                print(f"Nodo {node}: Comunità {community_id}")
        print()

    def Centralities(self):
        '''
        This function prints the values of different centrality measures:
        -Current flow betweenness centrality calculated thanks to the NetworkX function
        called "current_flow_betweenness_centrality()".
        -Edge current flow betweenness centrality calculated thanks to the NetworkX function
        called "edge_current_flow_betweenness_centrality()".
        -Current flow closeness centrality calculated thanks to the NetworkX function
        called "current_flow_closeness_centrality()".
        -Laplacian centrality calculated thanks to the NetworkX function
        called "laplacian_centrality()".
        Take a look of README.md for more information.
        '''
        currentflow = nx.current_flow_betweenness_centrality(
            self.graph, weight='weight')
        currentflow = sorted(currentflow.items(),
                             key=lambda x: x[1], reverse=True)
        print("Current flow betweenness centrality:")
        for node, centrality in currentflow:
            centrality = round(centrality, 3)
            print(f"{node}: {centrality}")
        print()

        edgecurrentflow = nx.edge_current_flow_betweenness_centrality(
            self.graph, weight='weight')
        edgecurrentflow = sorted(edgecurrentflow.items(),
                                 key=lambda x: x[1], reverse=True)
        print("Edge current flow betweenness centrality:")
        for edge, centrality in edgecurrentflow:
            centrality = round(centrality, 3)
            print(f"{edge}: {centrality}")
        print()

        currentflowcloseness = nx.current_flow_closeness_centrality(
            self.graph, weight='weight')
        currentflowcloseness = sorted(
            currentflowcloseness.items(), key=lambda x: x[1], reverse=True)
        print("Current flow closeness centrality:")
        for node, centrality in currentflowcloseness:
            centrality = round(centrality, 3)
            print(f"{node}: {centrality}")
        print()

        laplacian = nx.laplacian_centrality(self.graph, weight='weight')
        laplacian = sorted(laplacian.items(), key=lambda x: x[1], reverse=True)
        print("Laplacian centrality:")
        for node, centrality in laplacian:
            centrality = round(centrality, 3)
            print(f"{node}: {centrality}")
        print()
