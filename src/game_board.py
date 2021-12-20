from game_button import GameButton
from game_states import GameStates
from constants import DefaultConstants


class GameBoard:
    is_player_ones_turn = True

    def __init__(self, master, height_of_board=DefaultConstants.HEIGHT_OF_BOARD,
                 width_of_board=DefaultConstants.WIDTH_OF_BOARD,
                 player_one_color=DefaultConstants.PLAYER_ONE_COLOR,
                 player_two_color=DefaultConstants.PLAYER_TWO_COLOR, when_button_pressed=lambda: None):
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
                button['command'] = lambda button=button, board=self.board: self.__button_set_if_is_occupied(button)

    def __button_set_if_is_occupied(self, button):
        if button.set_if_is_occupied(self.board, self.is_player_ones_turn):
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
                    occupying_color = self.board[i][j]['bg']
                    if self.get_if_a_spot_wins(i, j, 1, 0) or \
                            self.get_if_a_spot_wins(i, j, 0, 1) or \
                            self.get_if_a_spot_wins(i, j, 1, 1) or \
                            self.get_if_a_spot_wins(i, j, 1, -1):
                        return self.get_game_state_from_color(occupying_color)
                else:
                    all_occupied = False
        if all_occupied:
            return GameStates.DRAW
        else:
            return GameStates.HAS_NOT_CONCLUDED

    # used to check vertically, horizontally, and diagonally if 4 of the same value exist
    def get_if_a_spot_wins(self, starting_height, starting_width, height_control, width_control):
        occupying_color = self.board[starting_height][starting_width]['bg']
        amount_located = 1
        # checks horizontally
        h = starting_height + height_control
        w = starting_width + width_control
        while self.height_of_board > h >= 0 and self.width_of_board > w >= 0:
            if self.board[h][w]['bg'] == occupying_color:
                amount_located += 1
                h += height_control
                w += width_control
            else:
                break
        h = starting_height - height_control
        w = starting_width - width_control
        while self.height_of_board > h >= 0 and self.width_of_board > w >= 0:
            if self.board[h][w]['bg'] == occupying_color:
                amount_located += 1
                h -= height_control
                w -= width_control
            else:
                break
        return amount_located >= 4

    # used to easily convert color string to game state for use in get_game_status
    def get_game_state_from_color(self, color):
        if color == self.player_one_color:
            return GameStates.PLAYER_ONE_WIN
        else:
            return GameStates.PLAYER_TWO_WIN
