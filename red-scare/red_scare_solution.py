import numpy as np
import math
import networkx as nx
from networkx import exception
import time

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
    

    def isCyclicUtil(self, v, visited, recStack):

        visited[v] = True
        recStack[v] = True

        for neighbour in range(len(self.adjecencyMatrix[v])):
            if not visited[neighbour] and self.adjecencyMatrix[v,neighbour] != 0:
                if self.isCyclicUtil(neighbour, visited, recStack):
                    return True
                elif recStack[neighbour]:
                    return True

        recStack[v] = False
        return False


    def isCyclic(self):
        visited = [False] * (int(self.n)+1)
        recStack = [False] * (int(self.n)+1)
        for node in range(int(self.n)):
            if not visited[node]:
                if self.isCyclicUtil(node,visited,recStack):
                    return True
        return False

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


        counter = 1
        for val in self.reds.values():
            #print(f"{counter} / {len(self.reds.keys())}")
            counter += 1
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
        return noneGraph.dijkstra(self.nodeDict[self.s], self.nodeDict[self.t])
        #return noneGraph.shortestPath(self.nodeDict[self.s], self.nodeDict[self.t])

    def alternate(self):
        alternateGraph = AlternateGraph(self.adjecencyMatrix, self.isRed, int(self.n))
        return alternateGraph.DFS(self.nodeDict[self.s], self.nodeDict[self.t])
        

if __name__ == "__main__":
    r = RedScare()
    noneTime = 0
    someTime = 0
    fewTime = 0
    manyTime = 0
    alternateTime = 0




    #print("None")
    tic = time.perf_counter()
    none = r.none()
    toc = time.perf_counter()
    noneTime = toc-tic

    if none == math.inf:
        none = -1
    #print("Few")
    tic = time.perf_counter()
    few = r.few()
    toc = time.perf_counter()
    fewTime = toc-tic

    if few == math.inf:
        few = -1

    #print("Alternate")
    tic = time.perf_counter()
    alternate = r.alternate()
    toc = time.perf_counter()
    alternateTime = toc-tic


    #print("some")
    if not r.isDirected:
        tic = time.perf_counter()
        some = r.some()
        toc = time.perf_counter()
        someTime = toc-tic

    else:
        some = "-"
        #print("Cant solve for directed Graphs")


    #print("many")
    if r.isDirected:
        if not r.isCyclic():
            tic = time.perf_counter()
            many = r.many()
            toc = time.perf_counter()
            manyTime = toc-tic
        else:
            many = "-"
            #print("Cant solve for cyclic Graphs")
    else:
        many = "-"
        #print("Cant solve for undirected Graphs")

    if many == -math.inf:
        many = -1

    print(f"None: {none} {noneTime:0.4f}s , Some: {some} {someTime:0.4f}s , Many: {many} {manyTime:0.4f}s , Few: {few} {fewTime:0.4f}s , Alternate: {alternate} {alternateTime:0.4f}s")