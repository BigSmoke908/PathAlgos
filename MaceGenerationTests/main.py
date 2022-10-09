import random
# script for trying out algorithms in Maze Generation (i'll probably port it to Rust later)


# used for Storing Mazes, can be called as if walls are infinitly small, but they are not
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
    def __init__(self, x, y):
        self.maze = [[0 for i in range(2 * y - 1)] for j in range(2 * x - 1)]  # has the number of "real" points that we want
        # 0 -> wall, 1 -> walkable space

    # gives the values of a certain point in the stored maze, only "real" points can be accessed
    def p(self, x, y):
        return self.maze[2 * x][2 * y]

    # sets the value of a real point
    def s(self, x, y, val=1):
        self.maze[2 * x][2 * y] = val

    # connects 2 points -> sets them and the connection in between to a value
    def c(self, x1, y1, x2, y2, val=1):
        self.maze[x1 * 2][y1 * 2] = val
        self.maze[x2 * 2][y2 * 2] = val
        self.maze[x1 + x2][y1 + y2] = val

    def printMaze(self):
        print('---')
        for row in self.maze:
            print(''.join([str(val) + ' ' for val in row]))
        print('---')

'''
def primsalgoMace(x, y):
    visited = []  # Coordinates of all already visited points

    while len(visited) != x //2 + y //2:
        pointer = visited[random.randrange(len(visited))]

        neighbours = [[pointer[0] - 1, pointer[1]], [pointer[]]]  # neighbours to this pointer
        if len(neighbours) == 0:  # no neighbours at this pointer
            continue
'''


m = Maze(2, 2)
m.printMaze()
# m.s(1, 1)
# m.printMaze()
m.c(*[1, 1], *[0, 1])
m.printMaze()
