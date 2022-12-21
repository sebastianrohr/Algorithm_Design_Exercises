import sys
import numpy as np
import math


class Graph:
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
        for i in range(n):
            for j in range(n):
                if self.og_graph[i, j] > 0 and self.graph[i, j] == 0 and visited[i] and not visited[j]:
                    print(i, j, self.og_graph[i, j])


if __name__ == "__main__":
    input = sys.stdin.readlines()
    input = [i.strip() for i in input]
    n = int(input[0].strip())  # number of nodes

    # create graph
    nodes = input[1:n+1]
    graph = np.zeros([n, n], dtype=float)
    m = int(input[n+1].strip())  # number of edges
    edges = [[int(j) for j in i.strip().split(" ")] for i in input[n+2:m+n+2]]

    # add edges to graph
    for edge in edges:
        if edge[2] == -1:
            graph[edge[0], edge[1]] = math.inf
            graph[edge[1], edge[0]] = math.inf
        else:
            graph[edge[0], edge[1]] = edge[2]
            graph[edge[1], edge[0]] = edge[2]

    fordFulkerson = Graph(graph, n)
    fordFulkerson.minCut(0, 54)
