import math

class TopGraph: # Topological
    def __init__(self, adj):
        self.adj = adj
        self.n = len(adj)
        self.stack = list()
        self.visited = [False] * self.n

    def topologicalSortUtil(self, v):
        self.visited[v] = True
        
        for i in self.adj[v]:
            if (not self.visited[i[0]]):
                self.topologicalSortUtil(i[0])

        self.stack.append(v)

    def longestPath(self,s,t):
        dist = [-math.inf] * self.n

        for i in range(self.n):
            if (self.visited[i] == False):
                self.topologicalsSortUtil(i)

        dist[s] = 0

        while (len(self.stack) > 0):
            u = self.stack.pop()

            if (dist[u] != math.inf):
                for i in self.adj[u]:
                    if (dist[i[0]] < dist[u] + i[1]):
                        dist[i[0]] = dist[u] + i[1]

        return dist[t]