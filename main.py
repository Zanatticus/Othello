from board import *
from logic import *
from tkinter import *

root = Tk()
game_screen = Canvas(root, width=500, height=500, background="#405336", highlightthickness=0)
game_screen.pack()

myBoard = Board(game_screen, root)

myBoard.display_board()
checkWin(myBoard.board_array)

game_screen.bind("<Button-1>", myBoard.click)
game_screen.bind("<Key>", myBoard.keyboard_buttons)
game_screen.focus_set()

root.title("Othello")
root.mainloop()
