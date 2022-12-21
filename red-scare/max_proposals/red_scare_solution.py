import numpy as np
from flow import FlowGraph
import math



class RedScare:
    def __init__(self):
     
        self.n, self.m, self.r = input().split(" ") # read the first line.

        self.nodes = [None] * int(self.n)
        self.nodeDict = {}
        self.reds = {}
        self.isDirected = False
        self.adjecencyMatrix = np.zeros((int(self.n), int(self.n)))
        
        self.s, self.t = input().split(" ")

        for i in range(int(self.n)):
            line = input().split(" ")
            self.nodes[i] = line[0]
            self.nodeDict[line[0]] = i

            if len(line) == 2:
                self.reds[line[0]] = i 

        for i in range(int(self.m)):
            line = input().split(" ")

            self.adjecencyMatrix[self.nodeDict[line[0]], self.nodeDict[line[2]]] = 1
            if line[1] == "--":
                self.adjecencyMatrix[self.nodeDict[line[2]], self.nodeDict[line[0]]] = 1
            else:
                self.isDirected = True
    

    def some(self):

        someGraph = np.zeros((int(self.n)+2,int(self.n)+2))
        for i in range(int(self.n)):
            for j in range(int(self.n)):
                someGraph[i,j] = self.adjecencyMatrix[i,j]

        someGraph[self.nodeDict[self.s],int(self.n)+1] = 1
        someGraph[self.nodeDict[self.t],int(self.n)+1] = 1

        for val in self.reds.values():
            _someGraph = np.copy(someGraph)
            
            _someGraph[int(self.n), val] = 2

            g = FlowGraph(_someGraph, int(self.n)+2)
            if g.FordFulkerson(int(self.n), int(self.n)+1) == 2:
                return True

        return False



if __name__ == "__main__":
    # solve "some" problem for undirected graphs
    r = RedScare()
    if not r.isDirected:
        print(r.some())
    else:
        print("Cant solve for directed Graphs")
        
    # Solve "many" problem for acyclic directed graphs
    