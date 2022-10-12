import json
import random
from PIL import Image
import time


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
    def __init__(self, x, y, w=0, c=1, searched=2, path=3, s=10):
        # values for walkable/non-walkable spaces
        self.wall = w
        self.corridor = c
        self.searched = searched
        self.path = path
        self.pixel = s  # number of pixels for one square in the maze (needed for turning the maze into a picture)
        # has the number of "real" points that we want
        self.maze = [[self.wall for i in range(2 * x - 1)] for j in range(2 * y - 1)]

    # checks, if you can go to a certain point
    def p(self, x, y):
        if y * 2 in range(len(self.maze)) and x * 2 in range(len(self.maze[0])):
            return self.maze[2 * y][2 * x] == self.wall
        return False

    # sets the value of a real point
    def s(self, x, y, val=None):
        if val is None:
            val = self.corridor
        self.maze[2 * y][2 * x] = val

    # connects 2 points -> sets them and the connection in between to a value
    def c(self, x1, y1, x2, y2, val=None):
        if val is None:
            val = self.corridor
        self.maze[y1 * 2][x1 * 2] = val
        self.maze[y2 * 2][x2 * 2] = val
        self.maze[y1 + y2][x1 + x2] = val

    def printMaze(self):
        print('---')
        for row in self.maze:
            print(''.join([str(val) + ' ' for val in row]))
        print('---')

    def picture(self, file, s=None):
        if s is None:
            s = self.pixel
        img = Image.new(mode="RGB", size=(len(self.maze[0]) * s, len(self.maze) * s))

        data = []
        for row in range(len(self.maze)):
            for i in range(s):
                for pixel in range(len(self.maze[row])):
                    for j in range(s):
                        if self.maze[row][pixel] == self.corridor:
                            data.append((255, 255, 255))
                        elif self.maze[row][pixel] == self.wall:
                            data.append((0, 0, 0))
                        elif self.maze[row][pixel] == self.searched:
                            data.append((255, 255, 0))
                        elif self.maze[row][pixel] == self.path:
                            data.append((255, 0, 0))
                        else:
                            data.append((0, 0, 255))
        img.putdata(data)
        img.save(file)

    def save(self, file):
        open(file, 'w').write(json.dumps(self.maze))

    def load(self, file):
        self.maze = json.loads(open(file).read())


# https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm (zuletzt besucht 9.10.2022, 11:03)
def generate(x, y):
    maze = Maze(x, y)
    # Coordinates of already visited points, the first one is the starting point
    visited = [[random.randrange(y), random.randrange(x)]]
    removed = 0
    while len(visited) + removed != x * y:  # as long as there are points, which are not part of the mace
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

        if len(n) == 1:  # this already is its last neighbour -> we not checking this point again will increase performance
            visited.remove(pointer)
            removed += 1

        neighbour = n[random.randrange(len(n))]  # the one we are connecting
        maze.c(*pointer, *neighbour)
        visited.append(neighbour)
    return maze


if __name__ == '__main__':
    begin = time.time()
    maze = generate(200, 200)
    maze.picture('maze.png')
    maze.save('maze.json')
    print(time.time() - begin)
