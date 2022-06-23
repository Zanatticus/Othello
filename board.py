from tkinter import *
from copy import deepcopy

# Global variables
move_number = 0
white_pieces = 2
black_pieces = 2
white_wins = 0
black_wins = 0
num_draws = 0
undo_counter = 0

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
        game_screen.delete("all")
        for x in range(8):
            for y in range(8):
                self.row = x
                self.column = y
                if self.board_array[x][y] == "W":
                    game_screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, fill="#aaa",
                                            outline="#aaa")
                    game_screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, fill="#fff",
                                            outline="#fff")

                elif self.board_array[x][y] == "B":
                    game_screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, fill="#000",
                                            outline="#000")
                    game_screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, fill="#111",
                                            outline="#111")
                game_screen.create_line(50 * (x + 1), 50 * (y + 1), 50 * 9, 50 * (y + 1))
                game_screen.create_line(50 * (x + 1), 50 * (y + 1), 50 * (x + 1), 50 * 9)
                self.display_valid_moves(x, y)
        game_screen.create_line(50, 50 * 9, 50 * 9, 50 * 9)
        game_screen.create_line(50 * 9, 50, 50 * 9, 50 * 9)
        count_pieces()
        self.display_scoreboard()
        if move_number % 2 == 0:
            game_screen.create_oval(22, 265, 32, 275, fill="lime")
            game_screen.create_oval(468, 265, 478, 275, fill="grey")
        else:
            game_screen.create_oval(468, 265, 478, 275, fill="lime")
            game_screen.create_oval(22, 265, 32, 275, fill="grey")

    def board_move(self, x, y):
        self.previous_array = self.board_array
        self.board_array = move(self.board_array, x, y)
        self.display_board()

        # Prevents calling checkWin() three times
        resultWin = checkWin()
        if resultWin == 1:
            game_screen.create_text(250, 470, text="WHITE WINS! Press 'R' to restart or 'Q' to quit.", fill="black",
                                    font=20)
        if resultWin == 2:
            game_screen.create_text(250, 470, text="BLACK WINS! Press 'R' to restart or 'Q' to quit.", fill="black",
                                    font=20)
        if resultWin == 3:
            game_screen.create_text(250, 470, text="DRAW! Press 'R' to restart or 'Q' to quit.", fill="black", font=20)

    # Function to be used to display available moves
    def display_valid_moves(self, x, y):
        global move_number
        if check_pass(self.board_array):
            move_number += 1
        validMoves = []
        for i in range(8):
            for j in range(8):
                if is_valid_move(self.board_array, x, y):
                    validMoves.append([x, y])
                    game_screen.create_oval(70 + 50 * x, 70 + 50 * y, 80 + 50 * x, 80 + 50 * y, fill="blue",
                                            outline="black")

    def display_scoreboard(self):
        game_screen.create_text(250, 25, text=f"White Wins - {white_wins} : {black_wins} - Black Wins", font=25)
        game_screen.create_text(25, 250, text=f"W:{white_pieces}", font=20)
        game_screen.create_text(475, 250, text=f"B:{black_pieces}", font=20)


def is_valid_move(given_array, x, y):
    global move_number
    if move_number % 2 == 0:
        player_color = "W"
    else:
        player_color = "B"
    # Checks for spots already taken
    if given_array[x][y] is not None:
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
        if not has_neighbors:
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
                    while (0 <= holdX <= 7) and (0 <= holdY <= 7):
                        if given_array[holdX][holdY] is None:
                            break
                        if given_array[holdX][holdY] == player_color:
                            forms_line = True
                            break
                        holdX = holdX + x_difference
                        holdY = holdY + y_difference

            return forms_line


def move(given_array, x, y):
    global move_number
    global white_pieces
    global black_pieces
    global undo_counter
    undo_counter = 1
    new_array = deepcopy(given_array)
    if move_number % 2 == 0:
        player_color = "W"
    else:
        player_color = "B"
    new_array[x][y] = player_color
    move_number += 1

    opposite_neighbors = []
    for i in range(max(0, x - 1), min(x + 2, 8)):
        for j in range(max(0, y - 1), min(y + 2, 8)):
            if given_array[i][j] is not None and given_array[i][j] != player_color:
                opposite_neighbors.append([i, j])

    for neighbor in opposite_neighbors:
        xVal = neighbor[0]
        yVal = neighbor[1]
        x_difference = xVal - x
        y_difference = yVal - y
        holdX = xVal
        holdY = yVal

        line_elements = []

        while 0 <= holdX <= 7 and 0 <= holdY <= 7:
            line_color = given_array[holdX][holdY]
            line_elements.append([holdX, holdY])
            if line_color is None:
                break
            if line_color == player_color:
                for piece in line_elements:
                    new_array[piece[0]][piece[1]] = player_color
                break
            # Continue down the line
            holdX = holdX + x_difference
            holdY = holdY + y_difference

    return new_array


# Function checks if a player needs to pass their turn. Used to check wins
def check_pass(given_array):
    global move_number
    validMoves = []
    for i in range(8):
        for j in range(8):
            if is_valid_move(given_array, i, j):
                validMoves.append([i, j])
    if len(validMoves) == 0:
        return True
    else:
        return False


def click(event):
    x = int((event.x - 50) / 50)
    y = int((event.y - 50) / 50)
    if 0 <= x <= 7 and 0 <= y <= 7:
        if is_valid_move(myBoard.board_array, x, y):
            myBoard.board_move(x, y)


def count_pieces():
    global white_pieces
    global black_pieces
    white_count = 0
    black_count = 0

    for i in range(8):
        for j in range(8):
            if myBoard.board_array[i][j] is None:
                continue
            elif myBoard.board_array[i][j] == "W":
                white_count += 1
            elif myBoard.board_array[i][j] == "B":
                black_count += 1
    white_pieces = white_count
    black_pieces = black_count

    return white_count, black_count


def undo():
    global move_number
    global undo_counter
    if undo_counter != 0:
        move_number -= 1
        myBoard.board_array = myBoard.previous_array
        myBoard.display_board()
        count_pieces()
        undo_counter = 0


def keyboard_buttons(event):
    button_pressed = event.keysym
    if button_pressed.lower() == "r":
        playNewGame()
    elif button_pressed.lower() == "q":
        root.destroy()
    elif button_pressed.lower() == "u":
        undo()


def playNewGame():
    global move_number
    global white_pieces
    global black_pieces
    move_number = 0
    white_pieces = 2
    black_pieces = 2
    game_screen.delete("all")
    myBoard.__init__()
    myBoard.display_board()


def checkWin():
    global black_wins
    global white_wins
    global num_draws
    global move_number

    if check_pass(myBoard.board_array):
        move_number += 1
        if check_pass(myBoard.board_array):
            num_pieces = count_pieces()

            if num_pieces[0] > num_pieces[1]:
                white_wins += 1
                return 1
            elif num_pieces[0] < num_pieces[1]:
                black_wins += 1
                return 2
            elif black_pieces == white_pieces:
                num_draws += 1
                return 3
    else:
        return 0


myBoard = Board()

myBoard.display_board()
checkWin()

game_screen.bind("<Button-1>", click)
game_screen.bind("<Key>", keyboard_buttons)
game_screen.focus_set()

root.title("Othello")
root.mainloop()
