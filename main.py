from board import *
from tkinter import *

root = Tk()
# Creates the window size and color which the game will be played on
game_screen = Canvas(root, width=500, height=500, background="#405336", highlightthickness=0)
game_screen.pack()

# Create a Board object and display it to start the game
myBoard = Board(game_screen, root)
myBoard.display_board()

# Allows for mouse clicks and keyboard inputs and focuses these inputs onto game_screen
game_screen.bind("<Button-1>", myBoard.click)
game_screen.bind("<Key>", myBoard.keyboard_buttons)
game_screen.focus_set()

root.title("Othello")
root.mainloop()
