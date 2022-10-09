import random
from PIL import Image
# script for trying out algorithms in Maze Generation (i'll probably port it to Rust later)


# is storing a Maze, we can call it as if the maze is walls of 0 width, does all the changing of it for us
class Maze:
    '''
    Format:
    o q o q o
    q   q   q
    o q o q o
    q   q   q
    o q o q o

    o -> Point with Coordinates in Maze
    q -> Possible Connection between 2 points in the maze
      -> cant be either, just always wall
    '''
    def __init__(self, x, y, w=0, c=1, s=10):
        # values for walkable/non-walkable spaces
        self.wall = w
        self.corridor = c
        self.pixel = s  # number of pixels for one square in the maze (needed for turning the maze into a picture)
        self.maze = [[self.wall for i in range(2 * y - 1)] for j in range(2 * x - 1)]
        # has the number of "real" points that we want

    # returns true if the spot is a wall, false if the spot is a corridor or not in the maze
    def p(self, x, y):
        if x * 2 in range(len(self.maze)) and y * 2 in range(len(self.maze[0])):
            return self.maze[2 * x][2 * y] == self.wall
        return False

    # sets the value of a real point
    def s(self, x, y, val=None):
        if val is None:
            val = self.corridor
        self.maze[2 * x][2 * y] = val

    # connects 2 points -> sets them and the connection in between to a value
    def c(self, x1, y1, x2, y2, val=None):
        if val is None:
            val = self.corridor
        self.maze[x1 * 2][y1 * 2] = val
        self.maze[x2 * 2][y2 * 2] = val
        self.maze[x1 + x2][y1 + y2] = val

    def printMaze(self):
        print('---')
        for row in self.maze:
            print(''.join([str(val) + ' ' for val in row]))
        print('---')

    def picture(self, file, s=None):
        if s is None:
            s = self.pixel
        img = Image.new(mode="RGB", size=(len(self.maze) * s, len(self.maze[0]) * s))

        data = []
        for row in range(len(self.maze)):
            for i in range(s):
                for pixel in range(len(self.maze[row])):
                    for j in range(s):
                        if self.maze[row][pixel] == self.corridor:
                            data.append((255, 255, 255))
                        else:
                            data.append((0, 0, 0))
        img.putdata(data)
        img.save(file)


# https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm (zuletzt besucht 9.10.2022, 11:03)
def primsalgoMace(x, y):
    maze = Maze(x, y)
    # Coordinates of already visited points, the first one is the starting point
    visited = [[random.randrange(x), random.randrange(y)]]
    counter = 0
    while len(visited) != x * y:  # as long as there are points not part of the mace
        pointer = visited[random.randrange(len(visited))]
        n = []  # neighbours for that pointer
        # point has to be in the maze, not already a connected, and not the pointer itself to be a neighbour
        if maze.p(pointer[0] - 1, pointer[1]):
            n.append([pointer[0] - 1, pointer[1]])
        if maze.p(pointer[0] + 1, pointer[1]):
            n.append([pointer[0] + 1, pointer[1]])
        if maze.p(pointer[0], pointer[1] - 1):
            n.append([pointer[0], pointer[1] - 1])
        if maze.p(pointer[0], pointer[1] + 1):
            n.append([pointer[0], pointer[1] + 1])

        if len(n) == 0:  # no available neighbours at that point
            continue

        neighbour = n[random.randrange(len(n))]  # the one we are connecting
        maze.c(*pointer, *neighbour)
        visited.append(neighbour)
        # if counter % 100 == 0:
        maze.picture('archive/' + str(counter) + '.png')
        counter += 1
    return maze


maze = primsalgoMace(50, 50)
maze.printMaze()
# maze.picture('final.png')
maze.picture('archive/2500.png')
