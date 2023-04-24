import networkx as nx
import matplotlib.pyplot as plt

# crea la rete complessa
G = nx.DiGraph()
G.add_edges_from([(1,2), (2,3), (2,4), (3,4), (4,5), (5,3)])

# disegna la rete
nx.draw(G, with_labels=True)

# mostra la rete
plt.show()
