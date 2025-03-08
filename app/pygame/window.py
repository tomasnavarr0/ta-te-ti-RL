from dataclasses import dataclass
import pygame

from .config import ALTO_VENTANA, ANCHO_VENTANA, AZUL, BLANCO, NEGRO, ROJO, TAMANO_CELDA

pygame.init()

@dataclass
class Window:
    window = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    font = pygame.font.Font(None, 80)
    pygame.display.set_caption("Tateti")

    @classmethod
    def draw_table(cls, board: list[list[str | None]]) -> None:
        cls.window.fill(BLANCO)

        for i in range(1, 3):
            pygame.draw.line(cls.window, NEGRO, (0, TAMANO_CELDA * i), (ANCHO_VENTANA, TAMANO_CELDA * i), 2)
            pygame.draw.line(cls.window, NEGRO, (TAMANO_CELDA * i, 0), (TAMANO_CELDA * i, ALTO_VENTANA), 2)

        for fila in range(3):
            for col in range(3):
                if board[fila][col] == "X":
                    texto = cls.font.render("X", True, ROJO)
                    cls.window.blit(texto, (col * TAMANO_CELDA + 30, fila * TAMANO_CELDA + 20))
                elif board[fila][col] == "O":
                    texto = cls.font.render("O", True, AZUL)
                    cls.window.blit(texto, (col * TAMANO_CELDA + 30, fila * TAMANO_CELDA + 20))
        pygame.display.flip()

    @staticmethod
    def get_cell(position: tuple[int, int]) -> tuple[int, int]:
        x, y = position
        fila = y // TAMANO_CELDA
        col = x // TAMANO_CELDA
        return fila, col
