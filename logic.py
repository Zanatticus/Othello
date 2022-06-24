from copy import deepcopy


class Logic:
    """
    The class associating to the Board class which handles all game logic
    """
    def __init__(self):
        """
        Initialization of variables
        """
        self.move_number = 0
        self.white_pieces = 2
        self.black_pieces = 2
        self.white_wins = 0
        self.black_wins = 0
        self.num_draws = 0
        self.undo_counter = 0

    def is_valid_move(self, given_array, x, y):
        """
        Returns True if the square selected is a valid move and False otherwise.
        :param given_array: matrix
        :param x: integer coordinate of given_array
        :param y: integer coordinate of given_array
        :return: boolean
        """

        if self.move_number % 2 == 0:
            player_color = "W"
        else:
            player_color = "B"
        # Checks for spots already taken
        if given_array[x][y] is not None:
            return False
        # Validity check for Othello rules: flanking/neighbors
        else:
            has_neighbors = False
            neighbors = []
            # Finds all neighbors
            for i in range(max(0, x - 1), min(x + 2, 8)):
                for j in range(max(0, y - 1), min(y + 2, 8)):
                    if given_array[i][j] is not None:
                        has_neighbors = True
                        neighbors.append([i, j])
            if not has_neighbors:
                return False
            else:
                # Creates a line stemming from the now found neighbors and determines if that is a valid line.
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

    def who_moves(self):
        """
        Determines which player's (white/black) move it is
        :return: integer
        """
        if self.move_number % 2 == 0:
            return 0
        else:
            return 1

    def move(self, given_array, x, y):
        """
        Places a new piece based on whose turn it is and also flips opponents pieces.
        :param given_array: matrix
        :param x: integer coordinate of given_array
        :param y: integer coordinate of given_array
        :return: matrix
        """
        self.undo_counter = 1
        new_array = deepcopy(given_array)
        if self.move_number % 2 == 0:
            player_color = "W"
        else:
            player_color = "B"
        new_array[x][y] = player_color
        self.move_number += 1

        opposite_neighbors = []
        # Finds all neighbors
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
                # Reached end of invalid line
                if line_color is None:
                    break
                # Reached end of valid line
                if line_color == player_color:
                    for piece in line_elements:
                        # Flips the opposite colored pieces
                        new_array[piece[0]][piece[1]] = player_color
                    break
                # Continues down the line
                holdX = holdX + x_difference
                holdY = holdY + y_difference

        return new_array

    def check_pass(self, given_array):
        """
        Function checks whether a player needs to pass their turn. Also used to check wins.
        :param given_array: matrix
        :return: boolean
        """
        validMoves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(given_array, i, j):
                    validMoves.append([i, j])
        if len(validMoves) == 0:
            return True
        else:
            return False

    def display_valid_moves(self, given_array, x, y):
        """
        Returns a list of lists containing x,y coordinates of all squares with valid placements.
        Used in board.py to display these locations on the board.
        :param given_array: matrix
        :param x: integer coordinate of given_array
        :param y: integer coordinate of given_array
        :return: list
        """
        if self.check_pass(given_array):
            self.move_number += 1
        validMoves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(given_array, x, y):
                    validMoves.append([x, y])
        return validMoves

    def count_pieces(self, given_array):
        """
        Counts up all white and black pieces and returns them as a tuple, respectively.
        :param given_array: matrix
        :return: tuple
        """
        white_count = 0
        black_count = 0

        for i in range(8):
            for j in range(8):
                if given_array[i][j] is None:
                    continue
                elif given_array[i][j] == "W":
                    white_count += 1
                elif given_array[i][j] == "B":
                    black_count += 1
        self.white_pieces = white_count
        self.black_pieces = black_count

        return white_count, black_count

    def undo(self):
        """
        Handles the logic behind performing an undo. Only capable of doing one undo before moving again.
        :return: None
        """
        if self.undo_counter != 0:
            self.move_number -= 1
            self.undo_counter = 0

    def play_new_game(self):
        """
        Restarts global variables to their initial state.
        :return:
        """
        self.move_number = 0
        self.white_pieces = 2
        self.black_pieces = 2

    def check_win(self, given_array):
        """
        Checks whether the game has ended based on if both players pass.
        Increments the number of wins or draws depending on how many
        pieces are on the board.
        :param given_array:
        :return:
        """
        # Checks for if the current player can't move
        if self.check_pass(given_array):
            self.move_number += 1
            # Checks for if the other player can't move
            if self.check_pass(given_array):
                num_pieces = self.count_pieces(given_array)
                if num_pieces[0] > num_pieces[1]:
                    self.white_wins += 1
                    return 1
                elif num_pieces[0] < num_pieces[1]:
                    self.black_wins += 1
                    return 2
                elif self.black_pieces == self.white_pieces:
                    self.num_draws += 1
                    return 3
        else:
            return 0

    def return_wins(self):
        """
        Returns a tuple containing the number of
        white wins and black wins, respectively.
        :return: tuple
        """
        return self.white_wins, self.black_wins
