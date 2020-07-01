import tkinter as tk
import sys
import random
import time

class Constants():
    TITLE = "Hamza le boss"

    WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080

    BOARD_LENGTH, BOARD_HEIGHT = 51, 51
    BOARD_MARGIN = 50

    START_POINT_COLOR = "blue"
    GOAL_POINT_COLOR = "red"
    WALL_POINT_COLOR = "black"
    PATH_COLOR = "#D58920"

    CASE_SIZE = 10


class Node():

    def __init__(self, position: tuple, parent, distance, heuristique):
        self.x, self.y = position[0], position[1]
        self.distance, self.heuristique = distance, heuristique

        self.total = self.distance + self.heuristique

        self.parent = parent


class Board(tk.Canvas):

    def __init__(self):
        super().__init__(width = Constants.WINDOW_WIDTH, height = Constants.WINDOW_HEIGHT)

        sys.setrecursionlimit(1000000000)

        self.init_board()
        self.pack()


    def init_board(self):

        self.board = [ [0] * Constants.BOARD_LENGTH ] * Constants.BOARD_HEIGHT
        self.walls = [ (x, y) for x in range(Constants.BOARD_LENGTH) for y in range(Constants.BOARD_HEIGHT) ]

        self.startPointX, self.startPointY = 0, 0
        self.goalPointX, self.goalPointY = 50, 50 

        self.startNode = Node((self.startPointX, self.startPointY), None, 0, 0)
        self.path = []

        self.mazeStarterPos = (0, 0)
        self.walls.remove(self.mazeStarterPos)
        self.visited = [self.mazeStarterPos]

        self.create_maze(self.mazeStarterPos)

        self.draw()

        self.find_path_aStar(self.startNode)

        self.draw()


    def create_maze(self, actual_pos):
        nei = self.find_nei(actual_pos)
        random.shuffle(nei)
        for n in nei:
            if n[0] in self.visited:
                continue
            if n[1] in self.visited:
                continue
            
            self.walls.remove(n[0])
            self.walls.remove(n[1])
            self.visited.append(n[0])
            self.visited.append(n[1])

            self.create_maze(n[1])


    def find_nei(self, position):
        x, y = position
        nei = []
        if x + 2 < Constants.BOARD_LENGTH:
            nei.append( [ (x+1, y), (x+2, y) ] )

        if x - 2 > -1:
            nei.append( [ (x-1, y), (x-2, y) ] )

        if y + 2 < Constants.BOARD_HEIGHT:
            nei.append( [ (x, y + 1), (x, y + 2) ] )

        if y - 2 > -1:
            nei.append( [ (x, y - 1), (x, y - 2) ] )

        return nei


    def find_path_aStar(self, actual_node):
        open_list = [actual_node]
        closed_list = []

        while len(open_list) > 0:
            current = open_list[0]
            open_list.pop(0)
            closed_list.append((current.x, current.y))

            if (current.x, current.y) == (self.goalPointX, self.goalPointY):
                while current.parent != self.startNode:
                    current = current.parent
                    self.path.append((current.x, current.y))
                return "END"
            
            voisin = self.neighbour_node(current.x, current.y, current, current.distance)
            voisin.sort(key=lambda x: x.heuristique)

            for next in voisin:
                if (next.x, next.y) in closed_list:
                    continue

                if (next.x, next.y) in self.walls:
                    continue
                    
                if next not in open_list:
                    open_list.append(next)

        return "IMPOSSIBLE"


    def neighbour_node(self, x, y, actual_node, distance):
        nei = []
        if(x + 1 < Constants.BOARD_LENGTH):
            heuristique = pow((self.goalPointX - x + 1), 2) + pow((self.goalPointY - y), 2)
            node = Node((x+1, y), actual_node, distance, heuristique)
            nei.append(node)

        if(x - 1 > -1):
            heuristique = pow((self.goalPointX - x - 1), 2) + pow((self.goalPointY - y), 2)
            node = Node((x-1, y), actual_node, distance, heuristique)
            nei.append(node)

        if(y + 1 < Constants.BOARD_HEIGHT):
            heuristique = pow((self.goalPointX - x), 2) + pow((self.goalPointY - y + 1), 2)
            node = Node((x, y+1), actual_node, distance, heuristique)
            nei.append(node)

        if(y - 1 > -1):
            heuristique = pow((self.goalPointX - x), 2) + pow((self.goalPointY - y - 1), 2)
            node = Node((x, y-1), actual_node, distance, heuristique)
            nei.append(node)

        return nei


    def draw(self):
        self.draw_path()
        self.draw_player()
        self.draw_goal()
        self.draw_board()
        self.draw_walls(self.walls)
        self.pack()


    def draw_player(self):
        pts = [self.startPointX * Constants.CASE_SIZE + Constants.BOARD_MARGIN, self.startPointY * Constants.CASE_SIZE + Constants.BOARD_MARGIN, 
        self.startPointX * Constants.CASE_SIZE + Constants.BOARD_MARGIN, (self.startPointY + 1) * Constants.CASE_SIZE + Constants.BOARD_MARGIN,
        (self.startPointX + 1) * Constants.CASE_SIZE + Constants.BOARD_MARGIN, (self.startPointY + 1) * Constants.CASE_SIZE - (Constants.CASE_SIZE / 2) + Constants.BOARD_MARGIN]

        self.create_polygon(pts, fill=Constants.START_POINT_COLOR)
        

    def draw_goal(self):
        self.create_oval(self.goalPointX * Constants.CASE_SIZE + Constants.BOARD_MARGIN, 
                        self.goalPointY * Constants.CASE_SIZE + Constants.BOARD_MARGIN, 
                        (self.goalPointX + 1) * Constants.CASE_SIZE + Constants.BOARD_MARGIN, 
                        (self.goalPointY + 1) * Constants.CASE_SIZE + Constants.BOARD_MARGIN, fill=Constants.GOAL_POINT_COLOR)
                        
    
    def draw_walls(self, lst):
        for tpl in lst:
            x, y = tpl[0], tpl[1]
            self.board[x][y] = 3
            self.create_rectangle(x * Constants.CASE_SIZE + Constants.BOARD_MARGIN,
                                y * Constants.CASE_SIZE + Constants.BOARD_MARGIN,
                                (x + 1) * Constants.CASE_SIZE + Constants.BOARD_MARGIN,
                                (y + 1) * Constants.CASE_SIZE + Constants.BOARD_MARGIN, fill=Constants.WALL_POINT_COLOR)


    def draw_board(self):
        for i in range(0, Constants.BOARD_LENGTH):
            for j in range(0, Constants.BOARD_HEIGHT):
                self.create_rectangle(i * Constants.CASE_SIZE + Constants.BOARD_MARGIN,
                                      j * Constants.CASE_SIZE + Constants.BOARD_MARGIN,
                                      (i + 1) * Constants.CASE_SIZE + Constants.BOARD_MARGIN,
                                      (j + 1) * Constants.CASE_SIZE + Constants.BOARD_MARGIN)


    def draw_path(self):
        for tpl in self.path:
            x, y = tpl[0], tpl[1]
            self.create_rectangle(x * Constants.CASE_SIZE + Constants.BOARD_MARGIN,
                            y * Constants.CASE_SIZE + Constants.BOARD_MARGIN,
                            (x + 1) * Constants.CASE_SIZE + Constants.BOARD_MARGIN,
                            (y + 1) * Constants.CASE_SIZE + Constants.BOARD_MARGIN, fill=Constants.PATH_COLOR)

        self.draw_player()
        self.draw_goal()

class Maze(tk.Frame):

    def __init__(self, master):
        super().__init__()

        master.title(Constants.TITLE)
        self.board = Board()
        self.pack()


if __name__ == "__main__":
    root = tk.Tk()
    maze = Maze(root)
    root.mainloop()
    pass
