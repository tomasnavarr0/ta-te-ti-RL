from dataclasses import dataclass, field


@dataclass
class Board:
    board: list[list[str]] = field(default_factory=lambda: [["" for _ in range(3)] for _ in range(3)])

    def show_board(self) -> None:
        for fila in self.board:
            print("|".join([casilla if casilla != "" else " " for casilla in fila]))
            print("-" * 5)

    def check_winner(self) -> str | None:
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.board[0][2]

        if all(casilla != "" for fila in self.board for casilla in fila):
            return "Draft"

        return None
