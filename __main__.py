import pygame
import sys
from app.tictactoe.movements import TicTacToeMovements
from app.pygame.window import Window


def main():
    board = TicTacToeMovements()
    window = Window()
    actual_player = "X"
    active_player = True

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and active_player:
                row, col = window.get_cell(evento.pos)
                if board.make_movement(row, col, actual_player):
                    winner = board.check_winner()
                    if winner:
                        active_player = False
                        if winner == "Draft":
                            print("Is a draft!")
                        else:
                            print(f"¡{winner} has won!")
                    actual_player = "O" if actual_player == "X" else "X"
        window.draw_table(board.board)


if __name__ == "__main__":
    main()
