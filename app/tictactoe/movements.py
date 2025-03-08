from .board import Board


class TicTacToeMovements(Board):
    def valid_movement(self, row: int, column: int) -> bool:
        return self.board[row][column] == ""

    def make_movement(self, row: int, column: int, player: str) -> bool:
        if self.valid_movement(row, column):
            self.board[row][column] = player
            self.turn += 1
            return True

        return False
