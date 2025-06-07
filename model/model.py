import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        # self._idProducts = {}
        # for prod in DAO.getAllProducts():
        #     self._idProducts[prod.Product_number] = prod
        self._idRetailers = {}
        for retailer in DAO.getAllRetailers():
            self._idRetailers[retailer.Retailer_code] = retailer

    def buildGraph(self, country, year):
        nodes = DAO.getAllNodes(country,self._idRetailers)
        self._grafo.add_nodes_from(nodes)
        edges = DAO.getAllEdges(country, self._idRetailers, year)
        for e in edges:
            if e.Retailer1 in self._grafo and e.Retailer2 in self._grafo:
                if self._grafo.has_edge(e.Retailer1, e.Retailer2):
                    self._grafo[e.Retailer1][e.Retailer2]['weight'] += e.peso
                else:
                    self._grafo.add_edge(e.Retailer1, e.Retailer2, weight=e.peso)

    def getGraph(self, country, year):
        grafo = self.buildGraph(country, year)
        return grafo

