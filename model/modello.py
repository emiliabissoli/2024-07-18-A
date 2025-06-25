import copy

import networkx as nx

from database.DAO import DAO
from model.gene import Gene


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._nodes = []
        self._idMapGene = {}
        self._archi = []
        self._camminoOttimo = []
        self._pesoOttimo = 0


    def buildGraph(self, cMin, cMax):
        self._graph.clear()
        self._nodes = DAO.getAllNodes(cMin, cMax)
        self._graph.add_nodes_from(self._nodes)
        self._idMapGene = {}
        for n in self._nodes:
            self._idMapGene[(n.GeneID,n.Function)] = n
        self.AddAllArchi(cMin,cMax)

    def AddAllArchi(self, cMin, cMax):
        self._archi = DAO.getAllArchi(cMin, cMax, self._idMapGene)
        for a in self._archi:
            self._graph.add_edge(a[0], a[1], weight = a[2])

    def getNumNodi(self):
        return self._graph.number_of_nodes()

    def getNumArchi(self):
        return self._graph.number_of_edges()


    def getNodiPesati(self):
        dati = []
        for n in self._nodes:
            successori = list(self._graph.successors(n))
            peso = 0
            for s in successori:
                peso += self._graph[n][s]["weight"]
            dati.append((n,len(successori), peso))

        dati.sort(key=lambda x: x[1], reverse = True)
        return dati[:5]


    def trovaCammino(self):
        self._camminoOttimo = []
        self._pesoOttimo = 0
        for n in self._graph.nodes():
            nuovi_successori = self._calcola_successori_ammissibili(n, [n])
            self._ricorsione([n], nuovi_successori)
        return self._camminoOttimo, self._pesoOttimo


    def _ricorsione(self, parziale,successori):
        #caso terminale
        if len(successori) == 0:
            if len(parziale) > len(self._camminoOttimo):
                self._camminoOttimo = copy.deepcopy(parziale)
                self._pesoOttimo = self._peso_cammino(self._camminoOttimo)
            elif len(parziale) == len(self._camminoOttimo) and self._peso_cammino(parziale) < self._pesoOttimo:
                self._camminoOttimo = copy.deepcopy(parziale)
                self._pesoOttimo = self._peso_cammino(self._camminoOttimo)

        # caso ricorsivo
        else:
            for s in successori:
                parziale.append(s)
                nuovi_successori = self._calcola_successori_ammissibili(s, parziale)
                self._ricorsione(parziale, nuovi_successori)
                parziale.pop()


    def _calcola_successori_ammissibili(self, n, parziale):
        last_essential = parziale[-1].Essential
        if len(parziale) == 1:
            nuovi_successori = []
            for i in list(self._graph.successors(n)):
                if i not in parziale and i.Essential != last_essential:
                    nuovi_successori.append(i)
        else:
            last_peso = self._graph.get_edge_data(parziale[-2], parziale[-1])["weight"]
            nuovi_successori = []
            for i in list(self._graph.successors(n)):
                if i not in parziale:
                    if i.Essential != last_essential:
                        edge_data = self._graph.get_edge_data(parziale[-1], i)
                        if edge_data is not None and edge_data["weight"] >= last_peso:
                            nuovi_successori.append(i)

        return nuovi_successori

    def _peso_cammino(self, cammino):
        peso = 0
        if len(cammino) == 1:
            return peso
        for i in range(0, len(cammino) - 1):
            peso += self._graph.get_edge_data(cammino[i], cammino[i + 1])["weight"]
        return peso

    def get_localizations(self):
        return DAO.get_all_localizations()