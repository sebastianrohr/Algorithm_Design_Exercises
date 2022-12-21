import numpy as np
import sys

class AdjacencyMatrix:
    def __init__(self, n: int): 
        self.n = n
        self.adjacencyMatrix = np.zeros((self.n, self.n), dtype=int)
        
    def addEdge(self, i, j, w):
        self.adjacencyMatrix[i][j] = w
    
    def addVertex(self):
        self.n += 1
        self.adjacencyMatrix = np.pad(self.adjacencyMatrix, ((0,1),(0,1)), 'constant', constant_values=0)
            

def parse_input():
    """Parse input from stdin and return a list of lines"""
    inp = sys.stdin.read().splitlines()
    
    n, m, r = [int(x) for x in inp[0].split(" ")] # number of nodes, number of edges, number of red nodes
    s, t = inp[1].split(" ") # source and target nodes
    vertices = [x for x in inp[2:2+n] if "*" not in x] # list of "normal" vertices
    red_vertices = [x for x in inp[2:2+n] if "*" in x] # list of red vertices
    edges = [x.split(" ") for x in inp[2+n:]] # list of edges
    return n, m, r, s, t, vertices, red_vertices, edges


    