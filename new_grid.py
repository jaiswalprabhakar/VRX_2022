import copy
import numpy as np
import cv2
import scipy
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

size=30
image1=cv2.imread("track2.png")
rows,cols,t=(image1.shape)
row_size=int(rows//size)
col_size=int(cols/size)
image= cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
image=cv2.resize(image,(size,size), fx=1, fy=1, interpolation= cv2.INTER_NEAREST)

image = cv2.bitwise_not(cv2.threshold(
            image, 200, 255, cv2.THRESH_BINARY)[1])
maze=scipy.array(image)
maze=(maze!=0).astype(int)
# print(image)
print(maze)
start = (size*2//3,size//2)
i=-1
n=0
for x in range(len(image[0])):
    if image[0][x]==0 and i==-1:
        i=x
        n+=1
    if image[0][x]==0:
        n+=1
print(i,n)
end = (0, i+n//2)
maze=maze.tolist()
path = astar(maze, start, end)
for i in range(len(path)-1):
    cv2.line(image1,(path[i][1]*col_size,path[i][0]*row_size),(path[i+1][1]*col_size,path[i+1][0]*row_size),(0,255,0),3)
cv2.imshow("iamge",image1)
cv2.waitKey(0)
print(path)





