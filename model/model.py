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
        self._bestPath = []
        self._nElementi = 0

    def path(self):

        self._bestPath = []
        self._nElementi = 0
        parziale = []

        essenziali = [n for n in self._graph.nodes() if n.Essential == "Essential"]
        essenziali.sort(key=lambda x: x.GeneID)

        non_essenziali = [n for n in self._graph.nodes() if n.Essential == "Non-Essential"]
        non_essenziali.sort(key=lambda x: x.GeneID)

        self._ricorsione(parziale, 0, essenziali)

        parziale = []

        self._ricorsione(parziale, 0, non_essenziali)

        return self._bestPath


    def _ricorsione(self, parziale, inizio_index, nodi):

        nElementi = len(parziale)

        if len(parziale) > self._nElementi:
            self._nElementi = nElementi
            self._bestPath = copy.deepcopy(parziale)

        elif len(parziale) == self._nElementi:
            best = self._graph.subgraph(self._bestPath)
            nuovoGrafo = self._graph.subgraph(parziale)
            bestCompConn = list(nx.connected_components(best))
            nuovoGrafoCompConn = list(nx.connected_components(nuovoGrafo))
            if len(bestCompConn) > len(nuovoGrafoCompConn):
                self._bestPath = parziale

        for i in range(inizio_index, len(nodi)):
            nodo_candidato = nodi[i]

            # Aggiungo il candidato
            parziale.append(nodo_candidato)

            # Chiamata ricorsiva: passo i + 1 così al prossimo giro valuterà solo i successivi
            self._ricorsione(parziale, i + 1, nodi)

            # Backtracking classico
            parziale.pop()


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
        return connOut

    def getNodiOrdinati(self):
        nodifiltrati = [n for n in self._graph.nodes() if n.Essential != "?"]
        nodifiltrati.sort(key=lambda x: x.GeneID)
        return nodifiltrati
