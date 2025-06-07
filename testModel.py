from model.model import Model

model = Model()
model.buildGraph("France", 2015)
print("Graph built successfully with color 'France'.")
print("Nodes in the graph:", model._grafo.number_of_nodes())
print("Edges in the graph:", model._grafo.number_of_edges())