from logic import *


class Board:
    """
    Board class handles all the displaying of the board to the screen and everything else associated with the board.
    """
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
        """
        Displays the board, scoreboard, whose move it is, etc.
        :return: None
        """
        self.game_screen.delete("all")
        for x in range(8):
            for y in range(8):
                self.row = x
                self.column = y
                # White piece display
                if self.board_array[x][y] == "W":
                    self.game_screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, fill="#aaa",
                                                 outline="#aaa")
                    self.game_screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, fill="#fff",
                                                 outline="#fff")
                # Black piece display
                elif self.board_array[x][y] == "B":
                    self.game_screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, fill="#000",
                                                 outline="#000")
                    self.game_screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, fill="#111",
                                                 outline="#111")
                # Board checker board lines
                self.game_screen.create_line(50 * (x + 1), 50 * (y + 1), 50 * 9, 50 * (y + 1))
                self.game_screen.create_line(50 * (x + 1), 50 * (y + 1), 50 * (x + 1), 50 * 9)
                # Blue circles for valid moves
                self.display_valid_moves(x, y)
        # Board boundaries
        self.game_screen.create_line(50, 50 * 9, 50 * 9, 50 * 9)
        self.game_screen.create_line(50 * 9, 50, 50 * 9, 50 * 9)
        count_pieces(self.board_array)
        # Scoreboard and number of pieces
        self.display_scoreboard()
        # Display of whose turn it is
        if not who_moves():
            self.game_screen.create_oval(22, 265, 32, 275, fill="lime")
            self.game_screen.create_oval(468, 265, 478, 275, fill="grey")
        else:
            self.game_screen.create_oval(468, 265, 478, 275, fill="lime")
            self.game_screen.create_oval(22, 265, 32, 275, fill="grey")

    def board_move(self, x, y):
        """
        Displays the result of logic.py's move function to the screen.
        :param x:
        :param y:
        :return:
        """
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

    def display_valid_moves(self, x, y):
        """
        Handles displaying all valid moves.
        :param x: integer coordinate of self.board_array
        :param y: integer coordinate of self.board_array
        :return: None
        """
        for valid_move in display_valid_moves(self.board_array, x, y):
            x = valid_move[0]
            y = valid_move[1]
            self.game_screen.create_oval(70 + 50 * x, 70 + 50 * y, 80 + 50 * x, 80 + 50 * y, fill="blue",
                                         outline="black")

    def display_scoreboard(self):
        """
        Handles displaying the scoreboard (wins) as well as the number of pieces currently on the board
        for both players.
        :return: None
        """
        wp = count_pieces(self.board_array)[0]
        bp = count_pieces(self.board_array)[1]
        ww = return_wins()[0]
        bw = return_wins()[1]
        self.game_screen.create_text(250, 25, text=f"White Wins - {ww} : {bw} - Black Wins", font=25)
        self.game_screen.create_text(25, 250, text=f"W:{wp}", font=20)
        self.game_screen.create_text(475, 250, text=f"B:{bp}", font=20)

    def click(self, event):
        """
        Handles mouse-click events on the board.
        :param event: mouse-click
        :return: None
        """
        x = int((event.x - 50) / 50)
        y = int((event.y - 50) / 50)
        if 0 <= x <= 7 and 0 <= y <= 7:
            if is_valid_move(self.board_array, x, y):
                self.board_move(x, y)

    def undo(self):
        """
        Updates the display after undo-ing a move
        :return: None
        """
        undo()
        self.board_array = self.previous_array
        self.display_board()
        count_pieces(self.board_array)

    def keyboard_buttons(self, event):
        """
        Handles keyboard input to either:
            a) restart
            b) quit
            c) undo
        :param event: keyboard input
        :return: None
        """
        button_pressed = event.keysym
        if button_pressed.lower() == "r":
            self.play_new_game()
        elif button_pressed.lower() == "q":
            self.root.destroy()
        elif button_pressed.lower() == "u":
            self.undo()

    def play_new_game(self):
        """
        Restarts the game.
        :return: None
        """
        play_new_game()
        self.game_screen.delete("all")
        self.__init__(self.game_screen, self.root)
        self.display_board()
