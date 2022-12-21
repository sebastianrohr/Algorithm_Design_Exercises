import numpy as np
import math


class FlowGraph:
    def __init__(self, graph, n):
        self.og_graph = np.copy(graph)
        self.graph = graph
        self.n = n

    def DFS(self, source, target, parent):
        # Deapth First Search to find a path from source to target
        queue = []
        queue.append(source)

        visited = [None] * self.n
        visited[source] = True

        while len(queue) > 0:  # while queue is not empty
            element = queue.pop()

            if element == target:
                return element

            # for each neighbor of element in graph
            for i, v in enumerate(self.graph[element]):
                if v != 0:  # if there is a path from element to i
                    if visited[i] is None:
                        visited[i] = True
                        parent[i] = element
                        queue.append(i)

        return False

    def FordFulkerson(self, source, target):
        # Returns the maximum flow from source to target

        parent = [-1] * self.n

        maxFlow = 0

        # while there is a path from source to target
        while self.DFS(source, target, parent):

            pathFlow = math.inf  # set pathFlow to infinity

            t = target

            while t != source:  # while we are not at the source
                pathFlow = min(pathFlow, self.graph[parent[t], t])
                t = parent[t]

            maxFlow += pathFlow

            t = target

            while t != source:  # update the residual graph
                self.graph[t, parent[t]] += pathFlow
                self.graph[parent[t], t] -= pathFlow

                t = parent[t]

        return maxFlow

    def minCut(self, source, target):
        # Returns the minimum cut from source to target

        maxFlow = self.FordFulkerson(source, target)
        print(maxFlow) # Print max flow

        # "visited array" to keep track of visited nodes
        visited = [False] * self.n
        visited[source] = True
        queue = []
        queue.append(source)

        while queue:  # while queue is not empty
            element = queue.pop()

            # for each neighbor of element in graph
            for i, v in enumerate(self.graph[element]):
                if v != 0:
                    if not visited[i]:
                        visited[i] = True
                        queue.append(i)

        # print the minimum cut
        for i in range(self.n):
            for j in range(self.n):
                if self.og_graph[i, j] > 0 and self.graph[i, j] == 0 and visited[i] and not visited[j]:
                    print(i, j, self.og_graph[i, j])