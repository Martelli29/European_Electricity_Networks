import networkx as nx


Nations = []
with open("DataSet/Nations.txt", "r") as file:
    next(file)  # skip first row
    row = next(file)  # second row
    Nations = row.strip().split(",")  # get name of the nations from the file


class DGraph:
    def __init__(self):
        self.graph=nx.DiGraph()
        for i in range(len(Nations)):
           self.graph.add_node(str(Nations[i]))

    def __len__(self):
        return len(self.graph)
    
    def edges(self):
        return self.graph.edges()
    
    def LinksCreation(self, WeightList):
        self.graph.add_weighted_edges_from(WeightList)

    def LinkDensity(self):
        density = nx.density(self.graph)
        density = round(density, 4)
        print("Density of the graph:", density)

    def Communities(self):
        partition = nx.community.greedy_modularity_communities(self.graph, weight='weight')

        # Stampa l'assegnazione delle comunità per ogni nodo
        print("Communitites:")
        for community_id, community in enumerate(partition):
            for node in community:
                print(f"Nodo {node}: Comunità {community_id}")

    def hits(self):
        hubs, authorities = nx.hits(
            self.graph, max_iter=100, tol=1e-15, nstart=None, normalized=True)
        hubs = sorted(hubs.items(), key=lambda x: x[1], reverse=True)
        authorities = sorted(authorities.items(), key=lambda x: x[1], reverse=True)

        hubs = [(node, round(value, 3)) for node, value in hubs]
        authorities = [(node, round(value, 3)) for node, value in authorities]

        print("Hubs:")
        for node, value in hubs:
            print(f"{node}: {value}")

        print("Authorities:")
        for node, value in authorities:
            print(f"{node}: {value}")


class UGraph:
    def __init__(self):
        self.graph=nx.Graph()
        for i in range(len(Nations)):
           self.graph.add_node(str(Nations[i]))

    def LinksCreation(self, WeightList):
        self.graph.add_weighted_edges_from(WeightList)

    def LinkDensity(self):
        density = nx.density()
        density = round(density, 4)
        print("Density of the graph:", density)

    def Communities(self, graph):
        partition = nx.community.greedy_modularity_communities(graph, weight='weight')

        # Stampa l'assegnazione delle comunità per ogni nodo
        print("Communitites:")
        for community_id, community in enumerate(partition):
            for node in community:
                print(f"Nodo {node}: Comunità {community_id}")

    def centralities(self, graph):
        currentflow = nx.current_flow_betweenness_centrality(graph, weight='weight')
        currentflow = sorted(currentflow.items(), key=lambda x: x[1], reverse=True)
        print("Current flow betweenness centrality:")
        for node, centrality in currentflow:
            centrality = round(centrality, 3)
            print(f"{node}: {centrality}")

        edgecurrentflow = nx.edge_current_flow_betweenness_centrality(
            graph, weight='weight')
        edgecurrentflow = sorted(edgecurrentflow.items(),
                                 key=lambda x: x[1], reverse=True)
        print("Edge current flow betweenness centrality:")
        for edge, centrality in edgecurrentflow:
            centrality = round(centrality, 3)
            print(f"{edge}: {centrality}")

        currentflowcloseness = nx.current_flow_closeness_centrality(
            graph, weight='weight')
        currentflowcloseness = sorted(
            currentflowcloseness.items(), key=lambda x: x[1], reverse=True)
        print("Current flow closeness centrality:")
        for node, centrality in currentflowcloseness:
            centrality = round(centrality, 3)
            print(f"{node}: {centrality}")

        laplacian = nx.laplacian_centrality(graph, weight='weight')
        laplacian = sorted(laplacian.items(), key=lambda x: x[1], reverse=True)
        print("Laplacian centrality:")
        for node, centrality in laplacian:
            centrality = round(centrality, 3)
            print(f"{node}: {centrality}")

