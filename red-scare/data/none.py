import math
import numpy as np
import networkx as nx

class NoneGraph:
    def __init__(self, adjMatrix, isRed, n):
        self.graph = np.zeros((n, n), dtype=int)
        self.n = n
        self.G = nx.DiGraph()
        self._n = 0
        self.indexMapping = dict()

        for i in range(int(self.n)):
            for j in range(int(self.n)):
                if isRed[i] or isRed[j]:
                    continue
                if adjMatrix[i,j] == 1:
                    self.G.add_edge(i,j)
                self.graph[i,j] = adjMatrix[i,j]

            if sum(self.graph[i]) != 0:
                self.indexMapping[i] =self._n
                self._n += 1

        self._graph = np.zeros((self._n, self._n), dtype=int)


        for i in range(int(self.n)):
            for j in range(int(self.n)):
                if self.graph[i,j] == 1:
                    self._graph[self.indexMapping[i],self.indexMapping[j]] = 1


    def minDistance(self, dist, sptSet):
        minimum = math.inf

        for u in range(self._n):
            print(minimum)
            if dist[u] < minimum and sptSet[u] == False:
                minimum = dist[u]
                min_index = u

        return min_index

    def dijkstra(self, s, t):
        dist = [math.inf] * self._n

        try:
            dist[self.indexMapping[s]] = 0
        except KeyError:
            return -1

        sptSet = [False] * self._n


        for cout in range(self._n):

            x = self.minDistance(dist, sptSet)

            sptSet[x] = True
            for y in self._graph[x]:
                if self._graph[x,y] > 0 and sptSet[y] == False and dist[y] > (dist[x] + self._graph[x,y]):
                    dist[y] = dist[x] + self._graph[x,y]
        try:
            return dist[t]
        except KeyError:
            return -1

    def shortestPath(self, s, t):
        return len(nx.shortest_path(self.G, source=s, target=t))-1