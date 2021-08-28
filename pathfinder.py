#!/usr/bin/python
"""
Date: 03.06.20 10:00
Author: lukas brunner
"""

"""
Full coverage path planing with the depth-first search (dfs) algorithm.
TODO: Description/Readme.md
TODO: Make repo
"""
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.sparse.csgraph import minimum_spanning_tree as mintree
import scipy.sparse as sp

import sys
#sys.setrecursionlimit(1500)

def printd(text):
    for i in text:
        print(i)
    input()


class PathFinder:
    def __init__(self, filename, diagonals = False):
        self.loadMapFromImage(filename)
        self.convertMap2Graph(diagonals)

        self.visited = set()
        self.pathList = list()
        self.dfsPathPlaner(self.graph, startingNode = self.xsize + 1)

    def loadMapFromImage(self, filename):
        self.image = np.array(Image.open(filename).convert("L"), np.int)
        self.image = self.image//self.image.max()
        print(self.image.shape)
        return self.image

    def convertMap2Graph(self, diagonals = False):
        self.ysize, self.xsize = int(self.image.shape[0]), int(self.image.shape[1])
        self.graph = dict()
        map = np.copy(self.image)
        counter = 0
        for yindex, y in enumerate(range(self.ysize)):
            for xindex, x in enumerate(range(self.xsize)):
                if not diagonals:
                    neighbours = [
                                    (yindex - 1, xindex), 
                                    (yindex, xindex - 1),
                                    (yindex, xindex + 1),
                                    (yindex + 1, xindex),
                                    ]
                else:
                    neighbours = [
                                    (yindex - 1, xindex - 1), 
                                    (yindex - 1, xindex), 
                                    (yindex - 1, xindex + 1), 
                                    (yindex, xindex - 1),
                                    (yindex, xindex + 1),
                                    (yindex + 1, xindex - 1),
                                    (yindex + 1, xindex),
                                    (yindex + 1, xindex + 1)
                                    ]

                if self.image[yindex][xindex] > 0:
                    connections = list()
                    try:
                        for y, x in neighbours:
                            if self.image[y][x] > 0:
                                absIndex = (y) * (self.xsize) + x
                                connections.append(absIndex)
                        self.graph[counter] = connections
                    except Exception as e:
                        print(e)
                else:   # node not reachable
                    pass
                counter += 1
        return self.graph
    
    def minSpanningTree(self):
        # experimental!
        self.vecGraph = np.zeros([self.xsize*self.ysize, self.xsize*self.ysize], dtype = int)
        for node, connections in self.graph.items():
            for connection in connections:
                self.vecGraph[node][connection] = node
        #print(self.vecGraph)
        path = mintree(self.vecGraph)
        #print(path)
        mPath = path.toarray().astype(int)

        pathindex = list()
        for yindex, y in enumerate(mPath):
            for xindex, x in enumerate(y):
                if x > 0:
                    pathindex.append(([yindex, xindex]))

        self.minGraph = dict()
        for node in self.graph.keys():
            for edge in pathindex:
                if node in edge:
                    self.minGraph[node] = edge

        return self.minGraph

    def dfsPathPlaner(self, graph, startingNode):
        #print(startingNode)
        if startingNode not in self.visited:
            self.pathList.append(startingNode)
            self.visited.add(startingNode)
            #print(startingNode)
            for neighbour in graph[startingNode]:
                self.dfsPathPlaner(graph, neighbour)

    def getPath(self):
        self.X = list()
        self.Y = list()
        for index in self.pathList:
            x = (index) % self.xsize
            y = (index) // self.xsize
            self.X.append(x)
            self.Y.append(y)
        return self.image, self.Y, self.X

def plot2x2Example():
    filenames = [
            "maps/grid0.png",
            "maps/grid1.png",
            "maps/grid2.png",
            "maps/grid3.png",
            ]
    fig, axs = plt.subplots(2, 2)
    fig.suptitle('Depth-search algorithm')
    counter = 0
    for i in range(2):
        for j in range(2):
            pathfinder = PathFinder(filenames[counter], diagonals = True)
            image, y, x = pathfinder.getPath()
            axs[i, j].imshow(image, cmap="gray")
            axs[i, j].plot(x,y, "-", c="r", linewidth=4)
            counter += 1
    plt.show()

def simplePlotExample():
    filename = "maps/big.png"
    pathfinder = PathFinder(filename, diagonals = False)
    image, y, x = pathfinder.getPath()
    #printd((y,x))
    plt.imshow(image, cmap="gray")
    plt.plot(x, y, "-", c="r", linewidth=4)
    plt.show()

def main():
    simplePlotExample()
    plot2x2Example()

if __name__ == "__main__":
    main()
