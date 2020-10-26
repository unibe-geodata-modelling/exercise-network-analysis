#importing the package
import networkx as nx
#initializing an empty (here undirected) graph
G = nx.Graph()
#adding nodes
G.add_node("Rome")
G.add_node("Bern")
G.add_node("Zurich")
G.add_node("Vienna")
G.add_node("Berlin")
G.add_node("Paris")

#adding edges between the nodes (undirected)
G.add_edge("Bern","Zurich", weight=120)
G.add_edge("Rome","Zurich", weight=946)
G.add_edge("Rome","Vienna", weight=1033)
G.add_edge("Rome","Paris", weight=1351)
G.add_edge("Rome","Berlin", weight=1469)
G.add_edge("Paris","Berlin", weight=991)
G.add_edge("Paris","Bern", weight=509)
G.add_edge("Vienna","Zurich", weight=672)
#show the graph
nx.draw(G, with_labels=True)
#nx.draw_circular(G, with_labels=True)
