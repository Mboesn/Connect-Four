from game_button import GameButton
from game_states import GameStates
from constants import DefaultConstants


class GameBoard:
    is_player_ones_turn = True

    def __init__(self, master=None, height_of_board=DefaultConstants.HEIGHT_OF_BOARD,
                 width_of_board=DefaultConstants.WIDTH_OF_BOARD,
                 player_one_color=DefaultConstants.PLAYER_ONE_COLOR,
                 player_two_color=DefaultConstants.PLAYER_TWO_COLOR, when_button_pressed=lambda: None,
                 board_to_copy=None, column_to_change=None):
        if master is None:
            self.copy(board_to_copy, column_to_change)
        else:
            self.height_of_board = height_of_board
            self.width_of_board = width_of_board
            self.player_one_color = player_one_color
            self.player_two_color = player_two_color
            self.when_button_pressed = when_button_pressed
            self.board = [[0 for i in range(width_of_board)] for j in range(height_of_board)]
            for i in range(height_of_board):
                for j in range(width_of_board):
                    button_below = None
                    if i > 0:
                        button_below = self.board[i - 1][j]
                    self.board[i][j] = GameButton(button_below, master, player_one_color=self.player_one_color,
                                                  player_two_color=self.player_two_color,
                                                  bg="white", height=3, width=6)
                    button = self.board[i][j]
                    pad = 5
                    button.grid(row=height_of_board - i, column=width_of_board - j, padx=pad, pady=pad)
                    button['command'] = lambda button=button, board=self.board: self.button_set_is_occupied(button)

    # this is used in order to create a none visible board using a board with one column changed
    def copy(self, board, column_to_change):
        self.height_of_board = board.height_of_board
        self.width_of_board = board.width_of_board
        self.player_one_color = board.player_one_color
        self.player_two_color = board.player_two_color
        self.is_player_ones_turn = not board.is_player_ones_turn
        self.board = [[0 for i in range(self.width_of_board)] for j in range(self.height_of_board)]
        for i in range(self.height_of_board):
            for j in range(self.width_of_board):
                button_below = None
                if i > 0:
                    button_below = self.board[i - 1][j]
                self.board[i][j] = GameButton(button_below)
                self.board[i][j].is_occupied = board.board[i][j].is_occupied
                self.board[i][j].is_occupied_by_first_player = board.board[i][j].is_occupied_by_first_player
        self.board[self.height_of_board - 1][column_to_change].set_is_occupied(self.board, self.is_player_ones_turn)

    def button_set_is_occupied(self, button):
        if button.set_is_occupied(self.board, self.is_player_ones_turn):
            self.is_player_ones_turn = not self.is_player_ones_turn
        self.when_button_pressed()

    # makes it so no more moves can be played
    def end_game(self):
        for i in range(self.height_of_board):
            for j in range(self.width_of_board):
                self.board[i][j]['command'] = lambda: None

    # gets a jagged list of a 6 x 7 board that is in a legal game state
    def get_game_status(self):
        all_occupied = True
        for i in range(self.height_of_board):
            for j in range(self.width_of_board):
                if self.board[i][j].is_occupied:
                    if self.get_if_a_spot_wins(i, j, 1, 0) or \
                            self.get_if_a_spot_wins(i, j, 0, 1) or \
                            self.get_if_a_spot_wins(i, j, 1, 1) or \
                            self.get_if_a_spot_wins(i, j, 1, -1):
                        if self.board[i][j].is_occupied_by_first_player:
                            return GameStates.PLAYER_ONE_WIN
                        else:
                            return GameStates.PLAYER_TWO_WIN
                else:
                    all_occupied = False
        if all_occupied:
            return GameStates.DRAW
        else:
            return GameStates.HAS_NOT_CONCLUDED

    # used to check vertically, horizontally, and diagonally if 4 of the same value exist
    def get_if_a_spot_wins(self, starting_height, starting_width, height_control, width_control):
        is_occupied_by_first_player = self.board[starting_height][starting_width].is_occupied_by_first_player
        amount_located = 1
        # checks horizontally
        h = starting_height + height_control
        w = starting_width + width_control
        while self.height_of_board > h >= 0 and self.width_of_board > w >= 0:
            if self.board[h][w].is_occupied and \
                    self.board[h][w].is_occupied_by_first_player == is_occupied_by_first_player:
                amount_located += 1
                h += height_control
                w += width_control
            else:
                break
        h = starting_height - height_control
        w = starting_width - width_control
        while self.height_of_board > h >= 0 and self.width_of_board > w >= 0:
            if self.board[h][w].is_occupied and \
                    self.board[h][w].is_occupied_by_first_player == is_occupied_by_first_player:
                amount_located += 1
                h -= height_control
                w -= width_control
            else:
                break
        return amount_located >= 4
