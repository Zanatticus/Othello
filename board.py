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
        print(self.board_array[x][y])
        self.previous_array = self.board_array
        self.display_board()

def update():
    myBoard = Board()
    myBoard.display_board()

def move(given_array, x, y):
    global move_number
    new_array = deepcopy(given_array)
    if move_number % 2 == 0:
        new_array[x][y] = "W"
    else:
        new_array[x][y] = "B"
    move_number += 1
    return new_array

def click(event):
    xClick = event.x
    yCick = event.y

    x = int((event.x - 50) / 50)
    y = int((event.y - 50) / 50)
    myBoard.board_move(x, y)
    print(x, y)



myBoard = Board()
myBoard.display_board()
game_screen.bind("<Button-1>", click)
# game_screen.bind("<Key>", key)
game_screen.update()


root.mainloop()
