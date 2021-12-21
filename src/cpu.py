from game_board import GameBoard
from game_button import GameButton
from game_states import GameStates


class Cpu:
    def calculate_min_max(self, board, depth, affect_board):
        if board.get_game_status() != GameStates.HAS_NOT_CONCLUDED or depth == 0:
            return board.get_game_status()

        possible_moves = []
        for i in range(board.width_of_board):
            if not board.board[board.height_of_board - 1][i].is_occupied:
                possible_moves.append(i)
        if board.is_player_ones_turn:
            best_eval = float('inf')
        else:
            best_eval = -float('inf')
        best_move = None
        for i in range(len(possible_moves)):
            possible_board = GameBoard(board_to_copy=board, column_to_change=possible_moves[i])
            possible_status = self.calculate_min_max(possible_board, depth - 1, False)
            if possible_status == GameStates.DRAW:
                possible_eval = 0
            else:
                possible_eval = possible_status
            if (possible_eval < best_eval) == board.is_player_ones_turn and (possible_eval != best_eval):
                best_eval = possible_eval
                best_move = possible_moves[i]
        if affect_board:
            board.button_set_is_occupied(board.board[board.height_of_board - 1][best_move])
        return best_eval
