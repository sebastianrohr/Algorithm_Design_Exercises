import math
import numpy as np
#import networkx as nx

class NoneGraph:
    def __init__(self, adjMatrix, isRed, n):
        self.graph = np.zeros((n, n), dtype=int)
        self.n = n

        for i in range(int(self.n)):
            for j in range(int(self.n)):
                if isRed[i] or isRed[j]:
                    continue
#                if adjMatrix[i,j] == 1:
#                    self.G.add_edge(i,j)
                self.graph[i,j] = adjMatrix[i,j]



    def minDistance(self, dist, sptSet):
        minimum = math.inf

        for u in range(self.n):
            if dist[u] < minimum and sptSet[u] == False:

                minimum = dist[u]
                min_index = u

        return min_index

    def dijkstra(self, s, t):
        dist = [math.inf] * self.n
        dist[s] = 0

        sptSet = [False] * self.n

        for cout in range(self.n):
            try:
                x = self.minDistance(dist, sptSet)
            except UnboundLocalError: # The node is disconnected
                continue 

            sptSet[x] = True
            for y in range(self.n):
                if self.graph[x,y] > 0 and sptSet[y] == False and dist[y] > dist[x] + self.graph[x,y]:
                    
                    dist[y] = dist[x] + self.graph[x,y]

        return dist[t]


#    def shortestPath(self, s, t):
#        return len(nx.shortest_path(self.G, source=s, target=t))-1