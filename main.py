from tkinter import *
from tkinter import ttk

board = Tk()
frame = ttk.Frame(board, padding=10)
frame.grid()
ttk.Label(frame, text="Othello").grid(column=1, row=0)
ttk.Button(frame, text="End Game", command=board.destroy).grid(column=1, row=1)
board.mainloop()#test
