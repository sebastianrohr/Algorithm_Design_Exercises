import math
import networkx as nx

class FewGraph:
    def __init__(self, adj):
        self.adj = adj
        self.n = len(adj)
        self.graph = [list()]*self.n


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

            for y in self.adj[x]:
                if sptSet[y[0]] == False and dist[y[0]] > dist[x] + y[1]:
                    dist[y[0]] = dist[x] + y[1]

        return dist[t]