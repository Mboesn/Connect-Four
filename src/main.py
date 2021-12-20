from tkinter import *
from game_state import GameState
from game_board import GameBoard
import tkinter.font

master = Tk()
master.title("Connect 4")
master.geometry("700x700")

game_state_text = StringVar()
game_state_text.set("player one's turn")
text_font = tkinter.font.Font(family="Comic Sans MS", size=30, weight="bold")
game_state_label = Label(master, textvariable=game_state_text, font=text_font)
game_state_label.grid(row=0, column=0, pady=10, padx=5, columnspan=7)
game_board = GameBoard(master, when_button_pressed=lambda: update_text())
game_state_label['bg'] = game_board.player_one_color


# updates the text at the top of the screen according to the gameState
def update_text():
    if game_board.get_game_status() == GameState.HAS_NOT_CONCLUDED:
        if game_board.is_player_ones_turn:
            set_text("player one's turn", game_board.player_one_color)
        else:
            set_text("player two's turn", game_board.player_two_color)
    elif game_board.get_game_status() == GameState.DRAW:
        set_text("draw", "white")
    else:
        if game_board.get_game_status() == GameState.PLAYER_ONE_WIN:
            set_text("player one won!!!", game_board.player_one_color)
        else:
            set_text("player two won!!!", game_board.player_two_color)
        game_board.end_game()


def set_text(text, color):
    global game_state_text
    global game_state_label
    game_state_text.set(text)
    game_state_label['bg'] = color


master.mainloop()
