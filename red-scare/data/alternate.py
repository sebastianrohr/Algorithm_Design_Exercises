import numpy as np


class AlternateGraph:
    def __init__(self, adjMatrix, isRed, n):
        self.graph = adjMatrix
        self.isRed = isRed
        self.n = n
    
    def DFS(self, source, target):
        queue = []
        queue.append(source)

        visited = [None] * self.n
        visited[source] = True

        while len(queue) > 0:  # while queue is not empty
            element = queue.pop()
            alternater = self.isRed[element]
            if element == target:
                return True

            # for each neighbor of element in graph
            for i, v in enumerate(self.graph[element]):
                

                if v != 0 and self.isRed[i] != alternater:  # if there is a path from element to i
                    if visited[i] is None:
                        visited[i] = True
                        queue.append(i)

        return False