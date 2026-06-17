import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._nodes = {}
        self._graph = nx.Graph()
        self._interactions = []
        self._allGenes = {}
        for i in DAO.get_all_genes():
            self._allGenes[i.GeneID] = i

    def getAllLocalizations(self):
        return DAO.getAllLocalizations()

    def creaGrafo(self, localization):

        self._graph.clear()
        self._nodes.clear()

        for i in DAO.get_all_nodes(localization):
            self._nodes[i.GeneID] = i
        self._graph.add_nodes_from(self._nodes.values())


        for u, v in DAO.getAllEdges(localization):
            if u in self._nodes and v in self._nodes:
                if self._graph.has_edge(self._nodes[u], self._nodes[v]):
                    continue
                else:
                    self._graph.add_edge(self._nodes[u], self._nodes[v])

        for u, v in self._graph.edges:
            if u.Chromosome == v.Chromosome:
                self._graph[u][v]['weight'] = u.Chromosome
            else:
                self._graph[u][v]['weight'] = u.Chromosome + v.Chromosome


    def getDettagliGrafo(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getSortedEdges(self):
        archi = list(self._graph.edges(data=True))
        archi.sort(key=lambda x: x[2]['weight'])
        return archi

    def getConnectedComponents(self):
        conn = list(nx.connected_components(self._graph))
        connOut = []
        for i in conn:
            if len(i) > 1:
                connOut.append(i)

        connOut.sort(key=lambda x: len(x), reverse=True)
        for i in connOut:
            print(i)
        return connOut
