from logic import *


class Board:

    def __init__(self, game_screen, root):
        """
        Initializes an 8x8 Othello board
        """
        self.game_screen = game_screen
        self.root = root
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
        self.game_screen.delete("all")
        for x in range(8):
            for y in range(8):
                self.row = x
                self.column = y
                if self.board_array[x][y] == "W":
                    self.game_screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, fill="#aaa",
                                                 outline="#aaa")
                    self.game_screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, fill="#fff",
                                                 outline="#fff")

                elif self.board_array[x][y] == "B":
                    self.game_screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, fill="#000",
                                                 outline="#000")
                    self.game_screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, fill="#111",
                                                 outline="#111")
                self.game_screen.create_line(50 * (x + 1), 50 * (y + 1), 50 * 9, 50 * (y + 1))
                self.game_screen.create_line(50 * (x + 1), 50 * (y + 1), 50 * (x + 1), 50 * 9)
                self.display_valid_moves(x, y)
        self.game_screen.create_line(50, 50 * 9, 50 * 9, 50 * 9)
        self.game_screen.create_line(50 * 9, 50, 50 * 9, 50 * 9)
        count_pieces(self.board_array)
        self.display_scoreboard()
        if not who_moves():
            self.game_screen.create_oval(22, 265, 32, 275, fill="lime")
            self.game_screen.create_oval(468, 265, 478, 275, fill="grey")
        else:
            self.game_screen.create_oval(468, 265, 478, 275, fill="lime")
            self.game_screen.create_oval(22, 265, 32, 275, fill="grey")

    def board_move(self, x, y):
        self.previous_array = self.board_array
        self.board_array = move(self.board_array, x, y)
        self.display_board()

        # Prevents calling checkWin() three times
        resultWin = checkWin(self.board_array)
        if resultWin == 1:
            self.game_screen.create_text(250, 470, text="WHITE WINS! Press 'R' to restart or 'Q' to quit.",
                                         fill="black",
                                         font=20)
        if resultWin == 2:
            self.game_screen.create_text(250, 470, text="BLACK WINS! Press 'R' to restart or 'Q' to quit.",
                                         fill="black",
                                         font=20)
        if resultWin == 3:
            self.game_screen.create_text(250, 470, text="DRAW! Press 'R' to restart or 'Q' to quit.", fill="black",
                                         font=20)

    # Function to be used to display available moves
    def display_valid_moves(self, x, y):
        for valid_move in display_valid_moves(self.board_array, x, y):
            x = valid_move[0]
            y = valid_move[1]
            self.game_screen.create_oval(70 + 50 * x, 70 + 50 * y, 80 + 50 * x, 80 + 50 * y, fill="blue",
                                         outline="black")

    def display_scoreboard(self):
        white_pieces = count_pieces(self.board_array)[0]
        black_pieces = count_pieces(self.board_array)[1]
        white_wins = return_wins()[0]
        black_wins = return_wins()[1]
        self.game_screen.create_text(250, 25, text=f"White Wins - {white_wins} : {black_wins} - Black Wins", font=25)
        self.game_screen.create_text(25, 250, text=f"W:{white_pieces}", font=20)
        self.game_screen.create_text(475, 250, text=f"B:{black_pieces}", font=20)

    def click(self, event):
        x = int((event.x - 50) / 50)
        y = int((event.y - 50) / 50)
        if 0 <= x <= 7 and 0 <= y <= 7:
            if is_valid_move(self.board_array, x, y):
                self.board_move(x, y)

    def undo(self):
        undo()
        self.board_array = self.previous_array
        self.display_board()
        count_pieces(self.board_array)

    def keyboard_buttons(self, event):
        button_pressed = event.keysym
        if button_pressed.lower() == "r":
            self.play_new_game()
        elif button_pressed.lower() == "q":
            self.root.destroy()
        elif button_pressed.lower() == "u":
            self.undo()

    def play_new_game(self):
        play_new_game()
        self.game_screen.delete("all")
        self.__init__(self.game_screen, self.root)
        self.display_board()
