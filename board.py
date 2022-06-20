from tkinter import *
from tkinter.ttk import *
from math import *
from time import *
from random import *
from copy import deepcopy

# Global variables
move_number = 0
white_pieces = 2
black_pieces = 2

root = Tk()
game_screen = Canvas(root, width=500, height=500, background="#405336", highlightthickness=0)
game_screen.pack()


class Board:

    def __init__(self):
        """
         Initializes an 8x8 Othello board
         """
        self.row = 0
        self.column = 0
        self.board_array = []
        for i in range(8):
            self.board_array.append([])
            for j in range(8):
                self.board_array[i].append(None)

        # Starting positions of an Othello board
        self.board_array[3][3] = "W"
        self.board_array[3][4] = "B"
        self.board_array[4][3] = "B"
        self.board_array[4][4] = "W"

        self.previous_array = self.board_array


    def display_board(self):
        for x in range(8):
            for y in range(8):
                self.row = x
                self.column = y
                if self.previous_array[x][y] == "W":
                    game_screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, tags="tile {0}-{1}".format(x, y), fill="#aaa", outline="#aaa")
                    game_screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, tags="tile {0}-{1}".format(x, y), fill="#fff", outline="#fff")

                elif self.previous_array[x][y] == "B":
                    game_screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, tags="tile {0}-{1}".format(x, y), fill="#000", outline="#000")
                    game_screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, tags="tile {0}-{1}".format(x, y), fill="#111", outline="#111")
                else:
                    game_screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, tags="tile {0}-{1}".format(x, y), fill="red", outline="red")
                    game_screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, tags="tile {0}-{1}".format(x, y), fill="grey", outline="grey")
                game_screen.create_line(50 * (x + 1), 50 * (y + 1), 50 * 9, 50 * (y + 1))
                game_screen.create_line(50 * (x + 1), 50 * (y + 1), 50 * (x + 1), 50 * 9)
        game_screen.create_line(50, 50 * 9, 50 * 9, 50 * 9)
        game_screen.create_line(50 * 9, 50, 50 * 9, 50 * 9)


# CHANGE BETWEEN PREVIOUS ARRAY AND BOARD ARRAY FOR UNDO FUNCTIONALITY?
    def board_move(self, x, y):
        self.board_array = move(self.board_array, x, y)
        print(self.board_array[x][y], "MOVE #:", move_number)
        self.previous_array = self.board_array
        self.display_board()

    #def neighbor_flip(self, x, y):


def update():
    myBoard = Board()
    myBoard.display_board()


def is_valid_move(given_array, x, y):
    print("test1")
    global move_number
    if move_number % 2 == 0:
        player_color = "W"
    else:
        player_color = "B"
    # Checks for spots already taken
    if given_array[x][y] is not None:
        print("INVALID: ALREADY HAVE PIECE")
        return False
    # Validity check for Othello rules: Flanking/neighbors
    else:
        has_neighbors = False
        neighbors = []
        for i in range(max(0, x - 1), min(x + 2, 8)):
            for j in range(max(0, y - 1), min(y + 2, 8)):
                if given_array[i][j] is not None:
                    has_neighbors = True
                    neighbors.append([i, j])
                    print("HAS A NEIGHBOR")
        print(neighbors)
        if not has_neighbors:
            print("INVALID: NO NEIGHBORS")
            return False
        else:
            forms_line = False
            for neighbor in neighbors:
                xVal = neighbor[0]
                yVal = neighbor[1]
                if given_array[xVal][yVal] == player_color:
                    continue
                else:
                    x_difference = xVal - x
                    y_difference = yVal - y
                    holdX = xVal
                    holdY = yVal
                    print("test2")
                    print("XDIFF =", x_difference)
                    print("YDIFF =", y_difference)
                    print("HOLDX =", holdX)
                    print("HOLDY =", holdY)
                    while (0 <= holdX <= 7) and (0 <= holdY <= 7):
                        if given_array[holdX][holdY] is None:
                            print("BREAK ON EMPTY")
                            break
                        if given_array[holdX][holdY] == player_color:
                            print("FORM LINE IS TRUE WOW")
                            forms_line = True
                            break
                        else:
                            print("TEST ELSE")
                            holdY = holdY + y_difference
                            holdX = holdX + x_difference # CANT BREAK> NEED TO FIX IT.
                        #holdX += x_difference
                        #holdX += y_difference
            print("FORMS_LINE =", forms_line)
            return forms_line


# Function to be used to display available moves TODO IMPLEMENT
def get_valid_moves(given_array, x, y):
    validMoves = []
    for i in range(8):
        for j in range(8):
            if is_valid_move(given_array, x, y):
                validMoves.append([x, y])
                game_screen.create_oval(54 + 50 * x, 54 + 50 * y, 66 + 50 * x, 66 + 50 * y, tags="tile {0}-{1}".format(x, y), fill="green", outline="#aaa")
    return validMoves


def move(given_array, x, y):
    global move_number
    #new_array = deepcopy(given_array) TODO DEEPCOPY OR NO?
    new_array = given_array
    if move_number % 2 == 0:
        new_array[x][y] = "W"
    else:
        new_array[x][y] = "B"
    move_number += 1
    return new_array


# TODO implement validity checking
def click(event):
    x = int((event.x - 50) / 50)
    y = int((event.y - 50) / 50)
    if is_valid_move(myBoard.board_array, x, y):
        myBoard.board_move(x, y)
        print(x, y)
    else:
        print("INVALID MOVE")



myBoard = Board()
myBoard.display_board()
game_screen.bind("<Button-1>", click)
# game_screen.bind("<Key>", key)
game_screen.update()


root.mainloop()
