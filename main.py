from tkinter import *
from enum import Enum
import tkinter.font

master = Tk()
master.title("Ya-boi")
master.geometry("700x700")
height_of_board = 6
width_of_board = 7
buttons = [[0 for i in range(width_of_board)] for j in range(height_of_board)]
is_player_ones_turn = True
player_one_color = 'blue'
player_two_color = 'red'
game_state_text = StringVar()
game_state_text.set("player one's turn")
text_font = tkinter.font.Font(family="Comic Sans MS", size=30, weight="bold")
game_state_label = Label(master, textvariable=game_state_text, font=text_font)
game_state_label['bg'] = player_one_color
game_state_label.grid(row=0, column=0, pady=10, padx=5, columnspan=width_of_board)


class GameState(Enum):
    has_not_concluded = 0
    player_one_win = 1
    player_two_win = -1
    draw = 2


class GameButton(Button, object):
    is_occupied = False
    is_occupied_by_first_player = False

    def _init_(self, button_below, master=None, cnf={}, **kw):
        super()._init_(master, cnf, **kw)
        self.button_below = button_below

    # places piece return true if legal returns false if illegal
    def set_if_is_occupied(self, board):
        if self.button_below is None or self.button_below.is_occupied:
            if not self.is_occupied:
                global is_player_ones_turn
                self.is_occupied_by_first_player = is_player_ones_turn

                if is_player_ones_turn:
                    global player_one_color
                    self['bg'] = player_one_color
                else:
                    global player_two_color
                    self['bg'] = player_two_color

                if get_game_status(board) == GameState.has_not_concluded:
                    if is_player_ones_turn:
                        set_text("player two's turn", player_two_color)
                    else:
                        set_text("player one's turn", player_one_color)
                elif get_game_status(board) == GameState.draw:
                    set_text("draw", "white")
                elif get_game_status(board) == GameState.player_one_win:
                    set_text("player one won!!!", player_one_color)
                    end_game(board)
                else:
                    set_text("player two won!!!", player_two_color)
                    end_game(board)

                is_player_ones_turn = not is_player_ones_turn
                self.is_occupied = True
        else:
            self.button_below.set_if_is_occupied(board)


def end_game(board):
    global height_of_board
    global width_of_board
    for i in range(height_of_board):
        for j in range(width_of_board):
            board[i][j]['command'] = lambda: None


def set_text(text, color):
    global game_state_text
    global game_state_label
    game_state_text.set(text)
    game_state_label['bg'] = color


for i in range(height_of_board):
    for j in range(width_of_board):
        button_below = None
        if i > 0:
            button_below = buttons[i - 1][j]
        buttons[i][j] = GameButton(button_below, master, bg="white", height=3, width=6)
        x = buttons[i][j]
        pad = 5
        x.grid(row=height_of_board - i, column=width_of_board - j, padx=pad, pady=pad)
        x['command'] = lambda x=x, buttons=buttons: x.set_if_is_occupied(buttons)


# gets a jagged list of a 6 x 7 board that is in a legal game state
def get_game_status(board):
    all_occupied = True
    for i in range(height_of_board):
        for j in range(width_of_board):
            if board[i][j].is_occupied:
                occupying_color = buttons[i][j]['bg']
                if get_if_a_spot_wins(board, i, j, 1, 0) or get_if_a_spot_wins(board, i, j, 0, 1) or get_if_a_spot_wins(
                        board, i, j, 1, 1):
                    return get_game_state_from_color(occupying_color)
            else:
                all_occupied = False
    if all_occupied:
        return GameState.draw
    else:
        return GameState.has_not_concluded


# used to easily convert color string to game state for use in get_game_status
def get_game_state_from_color(color):
    global player_one_color
    if color == player_one_color:
        return GameState.player_one_win
    else:
        return GameState.player_two_win


# used to check vertically, horizontally, and diagonally if 4 of the same value exist
def get_if_a_spot_wins(board, starting_height, starting_width, height_control, width_control):
    occupying_color = board[starting_height][starting_width]['bg']
    amount_located = 1
    # checks horizontally
    h = starting_height + height_control
    w = starting_width + width_control
    global width_of_board
    global height_of_board
    while height_of_board > h >= 0 and width_of_board > w >= 0:
        if board[h][w]['bg'] == occupying_color:
            amount_located += 1
            h += height_control
            w += width_control
        else:
            break
    h = starting_height - height_control
    w = starting_width - width_control
    while height_of_board > h >= 0 and width_of_board > w >= 0:
        if board[h][w]['bg'] == occupying_color:
            amount_located += 1
            h -= height_control
            w -= width_control
        else:
            break
    return amount_located >= 4


master.mainloop()