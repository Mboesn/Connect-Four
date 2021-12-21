from tkinter import *
from constants import DefaultConstants


class GameButton(Button, object):
    is_occupied = False
    is_occupied_by_first_player = False

    def __init__(self, button_below, master=None, player_one_color=DefaultConstants.PLAYER_ONE_COLOR,
                 player_two_color=DefaultConstants.PLAYER_TWO_COLOR, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.button_below = button_below
        self.player_one_color = player_one_color
        self.player_two_color = player_two_color

    # places piece return true if legal returns false if illegal
    def set_is_occupied(self, board, is_player_ones_turn):
        if self.button_below is None or self.button_below.is_occupied:
            if not self.is_occupied:
                self.is_occupied_by_first_player = is_player_ones_turn
                if is_player_ones_turn:
                    self['bg'] = self.player_one_color
                else:
                    self['bg'] = self.player_two_color
                self.is_occupied = True
                return True
            return False
        else:
            return self.button_below.set_is_occupied(board, is_player_ones_turn)
