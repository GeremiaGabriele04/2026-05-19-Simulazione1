import copy
import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._allNodes = []
        self._idMapArtist = {}
        self._bestPath = []
        self._bestScore = 0

    def getLongestPath(self, start):
        self._bestPath = []
        self._bestScore = 0
        parziale = [start]

        # Avviamo la ricorsione passando solo il cammino parziale
        self._ricorsione(parziale)
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        # Ogni volta che entriamo, verifichiamo se il cammino parziale attuale
        # ha un punteggio maggiore del record registrato finora.
        current_score = self._getScore(parziale)
        if current_score > self._bestScore:
            self._bestScore = current_score
            self._bestPath = copy.deepcopy(parziale)

        # Esploriamo i successori dell'ultimo nodo inserito nel cammino
        for n in self._graph.successors(parziale[-1]):
            # 'if n not in parziale' evita di entrare in loop infiniti (cicli)
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale)  # Chiamata ricorsiva pulita
                parziale.pop()              # Backtracking: toglie il nodo per provare altre strade

    def _getScore(self, parziale):
        score = 0
        for i in range(0, len(parziale) - 1):
            score += self._graph[parziale[i]][parziale[i+1]]['weight']
        return score

    def getLongestPathV2(self, start):
        self._bestPath = []
        self._bestScore = 0
        parziale = [start]

        self._ricorsioneV2(parziale)
        return self._bestPath, self._bestScore

    def _ricorsioneV2(self, parziale):
        # Controlliamo se il cammino attuale batte il record di punteggio
        current_score = self._getScore(parziale)
        if current_score > self._bestScore:
            self._bestScore = current_score
            self._bestPath = copy.deepcopy(parziale)

        # Recuperiamo il peso dell'ultimo arco preso (se il cammino ha almeno 2 nodi)
        ultimo_peso = None
        if len(parziale) >= 2:
            ultimo_peso = self._graph[parziale[-2]][parziale[-1]]['weight']

        # Esploriamo i successori
        for n in self._graph.successors(parziale[-1]):
            if n not in parziale:
                # Troviamo il peso del potenziale prossimo arco
                peso_prossimo_arco = self._graph[parziale[-1]][n]['weight']

                # Condizione chiave: se è il primo arco, passiamo sempre.
                # Se ci sono archi precedenti, il prossimo deve essere strettamente maggiore (>).
                if ultimo_peso is None or peso_prossimo_arco > ultimo_peso:
                    parziale.append(n)
                    self._ricorsioneV2(parziale)
                    parziale.pop()  # Backtracking


    def buildGraph(self, genre):
        self._graph.clear()
        self._graph.clear_edges()
        self._idMapArtist.clear()

        self._allNodes = DAO.getAllNodes(genre.GenreId)
        for a in self._allNodes:
            self._idMapArtist[a.ArtistId] = a

        self._graph.add_nodes_from(self._allNodes)
        self.addEdges(genre.GenreId)

    def addEdges(self, idGenre):
        dict = DAO.getAllEdges(idGenre, self._idMapArtist)
        popo = DAO.getAllPopo(idGenre, self._idMapArtist)
        listaAggiunti = []

        for k in dict.keys():
            listaCoppie = itertools.combinations(dict[k], 2)
            for c in listaCoppie:
                if (c[0], c[1]) in listaAggiunti or (c[1], c[0]) in listaAggiunti:
                    continue
                else:
                    a1 = self._idMapArtist[c[0]]
                    a2 = self._idMapArtist[c[1]]
                    pop1 = popo[c[0]]
                    pop2 = popo[c[1]]
                    if pop1>pop2:
                        self._graph.add_edge(a1, a2, weight=pop1+pop2)
                        listaAggiunti.append((c[0], c[1]))
                    if pop2>pop1:
                        self._graph.add_edge(a2, a1, weight=pop2+pop1)
                        listaAggiunti.append((c[1], c[0]))
                    if pop1==pop2:
                        self._graph.add_edge(a1, a2, weight=pop1 + pop2)
                        listaAggiunti.append((c[0], c[1]))
                        self._graph.add_edge(a2, a1, weight=pop2 + pop1)
                        listaAggiunti.append((c[1], c[0]))



    def getAllGenre(self):
        return DAO.getAllGenre()

    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumArchi(self):
        return len(self._graph.edges)

    def getArtists(self):
        return self._allNodes

    def getTop5(self):
        lista = sorted(self._graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
        return lista[:5]

    def getInfluente(self):
        lista = []
        for n in self._allNodes:
            sommaU = 0
            sommaE = 0
            listaU = self._graph.out_edges(n, data=True)
            listaE = self._graph.in_edges(n, data=True)
            for u,v,w in listaU:
                sommaU += w['weight']
            for u,v,w in listaE:
                sommaE += w['weight']
            lista.append((n, sommaU - sommaE))
        return sorted(lista, key=lambda x: x[1], reverse=True)[0]

