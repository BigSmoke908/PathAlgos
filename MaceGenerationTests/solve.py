import math
from generate import Maze
import random


class Solver:
    def __init__(self, m):
        self.maze = m

    def dist(self, x1, y1, x2, y2):
        return int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) * 10)

    def astar(self, source, destination):
        wrongsource = source[0] not in range(len(self.maze[0])) or source[1] not in range(len(self.maze))
        wrongdestination = destination[0] not in range(len(self.maze[0])) or destination[1] not in range(len(self.maze))
        if wrongsource or wrongdestination:
            print("Start und Ende müssen innerhalb von dem Maze liege")
            return None
        if self.maze[source[1]][source[0]] != 1 or self.maze[destination[1]][destination[0]] != 1:
            print("Start und Ende dürfen nicht auf einer Wand liegen")
            return None

        # cost to reach a tile
        costmap = [[float('inf') for k in range(len(self.maze[0]))] for l in range(len(self.maze))]
        pointer = source.copy()
        costmap[pointer[1]][pointer[0]] = 0
        visited = []

        while pointer != destination:
            # find all neighbours to that point, calculate their costs
            # (Cost = dist to current cell + current cell cost + dist to destination)
            for i in range(-1, 2):  # the offsets to get all neighbours
                for j in range(-1, 2):
                    n = [pointer[0] + i, pointer[1] + j]
                    # neighbour on the map?
                    if n[0] in range(len(costmap[0])) and n[1] in range(len(costmap)):
                        if i != 0 or j != 0:  # actually a new point
                            if n[0] != source[0] or n[1] != source[1]:  # dont calculate for the start
                                if self.maze[n[1]][n[0]] != 0:
                                    costmap[n[1]][n[0]] = min(costmap[pointer[1]][pointer[0]] + self.dist(*n, *pointer) + self.dist(*n, *destination), costmap[n[1]][n[0]])

            # set pointer to the new position (lowest cost to get there and not yet visited)
            visited.append(pointer)
            nextpointer = [pointer[0], pointer[1], float('inf')]
            for row in range(len(costmap)):
                for tile in range(len(costmap[row])):
                    if costmap[row][tile] < nextpointer[2] and [tile, row] not in visited:
                        nextpointer = [tile, row, costmap[row][tile]]

            if nextpointer[2] == float('inf'):
                print("der Weg konnte nicht gefunden werden")
                return
            pointer = [nextpointer[0], nextpointer[1]].copy()

        # retrace the path now
        path = []
        while pointer != source:
            path.append(pointer)

            npointer = [0, 0, float('inf')]
            # find the neighbour with the lowest value
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i != 0 or j != 0:
                        n = [pointer[0] + i, pointer[1] + j]
                        if n[0] in range(len(costmap[0])) and n[1] in range(len(costmap)) and n not in path:
                            if costmap[n[1]][n[0]] + self.dist(*n, *pointer) < npointer[2]:
                                npointer = [n[0], n[1], costmap[n[1]][n[0]]]
            pointer = [npointer[0], npointer[1]]
        return path


storage = Maze(5, 5)
storage.load('maze.json')
maze = storage.maze
solver = Solver(maze)
dest = [58, 58]
PATH = solver.astar([0, 0], dest)
for point in PATH:
    storage.maze[point[1]][point[0]] = 2
storage.maze[0][0] = 2
storage.maze[dest[1]][dest[0]] = 2
storage.picture('solved.png')
