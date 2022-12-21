import numpy as np
import math
import networkx as nx
from networkx import exception

from flow import FlowGraph
from top import TopGraph
from dijkstra import FewGraph
from none import NoneGraph
from alternate import AlternateGraph


class RedScare:
    def __init__(self):
     
        self.n, self.m, self.r = input().split(" ") # read the first line.

        self.nodes = [None] * int(self.n)
        self.nodeDict = {}
        self.reds = {}
        self.isRed = [False] * int(self.n)
        self.isDirected = False
        self.adjecencyMatrix = np.zeros((int(self.n), int(self.n)))
        
        self.s, self.t = input().split(" ")

        for i in range(int(self.n)):
            line = input().split(" ")
            self.nodes[i] = line[0]
            self.nodeDict[line[0]] = i

            if len(line) == 2:
                self.reds[line[0]] = i 
                self.isRed[i] = True
        for i in range(int(self.m)):
            line = input().split(" ")

            self.adjecencyMatrix[self.nodeDict[line[0]], self.nodeDict[line[2]]] = 1
            if line[1] == "--":
                self.adjecencyMatrix[self.nodeDict[line[2]], self.nodeDict[line[0]]] = 1
            else:
                self.isDirected = True
    
    def getNoneAdjList(self):
        adj = [[] for i in range(int(self.n))]
        
        for i in range(int(self.n)):
            for j in range(int(self.n)):
                if self.adjecencyMatrix[i,j] == 1:
                    if self.isRed[j] or self.isRed[i]:
                        continue
                    else:
                        adj[i].append([j,1])


    def getReWeightedAdjList(self):
        adj = [[] for i in range(int(self.n))]
        
        for i in range(int(self.n)):
            for j in range(int(self.n)):
                if self.adjecencyMatrix[i,j] == 1:
                    if self.isRed[j]:
                        adj[i].append([j,1])
                    else:
                        adj[i].append([j,0])

        return adj
    
    def isCyclic(self):
        G = nx.from_numpy_matrix(self.adjecencyMatrix, create_using=nx.MultiGraph)

        try:
            nx.find_cycle(G, orientation="original") # Uses DFS
        except exception.NetworkXNoCycle:
            return False

        return True

    def some(self):

        n = (int(self.n)+2)
        someGraph = np.zeros((n*2,n*2))

        for i in range(int(self.n)):
            someGraph[i+n,i] = 1
            for j in range(int(self.n)):
                someGraph[i,j+n] = self.adjecencyMatrix[i,j]
                
        someGraph[self.nodeDict[self.s],int(self.n)+1+n] = 1
        someGraph[self.nodeDict[self.t],int(self.n)+1+n] = 1

        someGraph[int(self.n)+1+n,int(self.n)+1] = 2

        for val in self.reds.values():
            _someGraph = np.copy(someGraph)

            _someGraph[int(self.n), val+n] = 2
            _someGraph[val+n,val] = 2

            g = FlowGraph(_someGraph, n*2)
            if g.FordFulkerson(int(self.n), int(self.n)+1) == 2:
                return True

        return False


    def many(self):
        adj = self.getReWeightedAdjList()
        topGraph = TopGraph(adj)
        return topGraph.longestPath(self.nodeDict[self.s], self.nodeDict[self.t])
        
    def few(self):
        adj = self.getReWeightedAdjList()
        fewGraph = FewGraph(adj)
        return fewGraph.dijkstra(self.nodeDict[self.s], self.nodeDict[self.t])

    def none(self):

        noneGraph = NoneGraph(self.adjecencyMatrix, self.isRed, int(self.n))
        #return noneGraph.dijkstra(self.nodeDict[self.s], self.nodeDict[self.t])
        return noneGraph.shortestPath(self.nodeDict[self.s], self.nodeDict[self.t])

    def alternate(self):
        alternateGraph = AlternateGraph(self.adjecencyMatrix, self.isRed, int(self.n))
        return alternateGraph.DFS(self.nodeDict[self.s], self.nodeDict[self.t])
        

if __name__ == "__main__":
    r = RedScare()

    none = r.none()
    if none == math.inf:
        none = -1

    few = r.few()
    if few == math.inf:
        few = -1


    alternate = r.alternate()


    if not r.isDirected:
        some = r.some()
    else:
        some = "-"
        #print("Cant solve for directed Graphs")

    if r.isDirected:
        if not r.isCyclic():
            many = r.many()
        else:
            many = "-"
            #print("Cant solve for cyclic Graphs")
    else:
        many = "-"
        #print("Cant solve for undirected Graphs")

    if many == -math.inf:
        many = -1

    print(f"None: {none} , Some: {some} , Many: {many} , Few: {few} , Alternate: {alternate}")