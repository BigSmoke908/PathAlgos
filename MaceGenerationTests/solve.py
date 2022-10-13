import math
import random
from generate import Maze
import time


class Solver:
    def __init__(self, m):
        self.maze = m

    # checks if a point is walkable
    def p(self, x, y):
        if x in range(len(self.maze[0])) and y in range(len(self.maze)):
            return self.maze[y][x] == 1
        return False

    def check_args(self, source, destination):
        wrongsource = source[0] not in range(len(self.maze[0])) or source[1] not in range(len(self.maze))
        wrongdestination = destination[0] not in range(len(self.maze[0])) or destination[1] not in range(len(self.maze))
        if wrongsource or wrongdestination:
            print("Start und Ende müssen innerhalb von dem Maze liege")
            return None
        if self.maze[source[1]][source[0]] != 1 or self.maze[destination[1]][destination[0]] != 1:
            print("Start und Ende dürfen nicht auf einer Wand liegen")
            return None

    # pythagorean distance does not work for astar TODO: why?
    def dist(self, x1, y1, x2, y2):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return 14 * min(dx, dy) + max(dx, dy) * 10

    def astar(self, source, destination):1
        self.check_args(source, destination)

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
                            if n[0] != source[0] or n[1] != source[1]:  # dont calculate for the source
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
                            cost = costmap[n[1]][n[0]] + self.dist(*n, *pointer)  # cost to get to that point
                            if cost < npointer[2]:
                                npointer = [n[0], n[1], cost]
            pointer = [npointer[0], npointer[1]]
        return path

    def dfs(self, source, destination):
        self.check_args(source, destination)
        path = [source]  # the path from the source to our pointer
        checked = []  # all tiles that where part of the path once, but are not leading to the destination
        pointer = source.copy()

        while pointer != destination:
            # at first we walk as deep into the maze as possible, Turning Order: Right, Up, Left, Down
            # check for walkable neighbouring tiles, (have to be walkable/not in the path/not in a previous path)
            if self.p(pointer[0] + 1, pointer[1]) and [pointer[0] + 1, pointer[1]] not in checked and [pointer[0] + 1, pointer[1]] not in path:
                pointer = [pointer[0] + 1, pointer[1]]
                path.append(pointer)
            elif self.p(pointer[0], pointer[1] - 1) and [pointer[0], pointer[1] - 1] not in checked and [pointer[0], pointer[1] - 1] not in path:
                pointer = [pointer[0], pointer[1] - 1]
                path.append(pointer)
            elif self.p(pointer[0] - 1, pointer[1]) and [pointer[0] - 1, pointer[1]] not in checked and [pointer[0] - 1, pointer[1]] not in path:
                pointer = [pointer[0] - 1, pointer[1]]
                path.append(pointer)
            elif self.p(pointer[0], pointer[1] + 1) and [pointer[0], pointer[1] + 1] not in checked and [pointer[0], pointer[1] + 1] not in path:
                pointer = [pointer[0], pointer[1] + 1]
                path.append(pointer)
            else:  # we have reached the end of this path and have to go back until we reach a junction to take another path
                if len(path) <= 1:
                    print('es gibt keinen Weg zu dem Ziel')
                    return
                checked.append(pointer)
                path.pop(-1)
                pointer = path[-1]
        return path


begin = time.time()
storage = Maze(5, 5)
storage.load('maze.json')
maze = storage.maze
solver = Solver(maze)
Source = [0, 0]
dest = [78, 78]
# PATH = solver.astar(Source, dest)
PATH = solver.dfs(Source, dest)
for point in PATH:
    storage.maze[point[1]][point[0]] = 3
storage.maze[Source[1]][Source[0]] = 2
storage.maze[dest[1]][dest[0]] = 2
storage.picture('solved.png')
print(time.time() - begin)
