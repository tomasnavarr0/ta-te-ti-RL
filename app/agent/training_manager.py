from dataclasses import dataclass, field
import sys
from typing import List, Tuple, Optional
import pickle
import pygame
from tqdm import tqdm
from app.agent.q_learning import QLearningAgent
from app.pygame.window import Window
from app.tictactoe.movements import TicTacToeMovements


@dataclass
class TrainingManager:
    agent1: QLearningAgent = field(default_factory=QLearningAgent())
    agent2: QLearningAgent = field(default_factory=QLearningAgent())
    win_rates: list[tuple[float, float]] = field(default_factory=list)
    visualize: bool = field(default=False)
    window: Window = field(init=False)
    
    def __post_init__(self):
        """Inicializar ventana solo si se requiere visualización"""
        self.window = Window() if self.visualize else None

    def _get_available_actions(self, state: list[list[str]]) -> list[tuple[int, int]]:
        return [(r, c) for r in range(3) for c in range(3) if state[r][c] == ""]

    def train_dueling_agents(self, episodes: int = 10000, save_path: str = "best_agent.pkl"):
        for episode in tqdm(range(episodes)):
            game = TicTacToeMovements()
            game_over = False
            agents = {"X": self.agent1, "O": self.agent2}
            
            # Configurar ventana si es necesario
            if self.visualize:
                self.window.window = pygame.display.set_mode((300, 500))  # Alto extra para stats
            
            while not game_over:
                # Manejar eventos y renderizar
                if self.visualize:
                    self._handle_pygame_events()
                    self._render_training(episode, game)
                
                # Lógica del juego
                current_player = "X" if game.turn % 2 == 0 else "O"
                agent = agents[current_player]
                state = [row.copy() for row in game.board]
                available = self._get_available_actions(state)
                
                if not available:
                    break
                
                action = agent.choose_action(state, available)
                prev_state = [row.copy() for row in state]
                game.make_movement(*action, current_player)
                winner = game.check_winner()
                
                reward = self._calculate_reward(winner, current_player, game)
                next_state = [row.copy() for row in game.board] if not winner else None
                agent.update(prev_state, action, reward, next_state)
                
                if winner:
                    self._update_win_stats(winner)
                    game_over = True

            # Rotar agentes y guardar progreso
            if episode % 100 == 0:
                self.agent1, self.agent2 = self.agent2, self.agent1
            
            if episode % 1000 == 0:
                self.save_best_agent(save_path)

    def _handle_pygame_events(self):
        """Mantener responsive la ventana durante el entrenamiento"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _render_training(self, episode: int, game: TicTacToeMovements):
        """Dibujar tablero y estadísticas de entrenamiento"""
        self.window.window.fill((255, 255, 255))
        self.window.draw_table(game.board)
        
        # Estadísticas
        font = pygame.font.Font(None, 24)
        stats = [
            f"Episodio: {episode}",
            f"Victorias X: {self.agent1.wins}",
            f"Victorias O: {self.agent2.wins}",
            f"Exploración X: {self.agent1.epsilon:.2f}",
            f"Exploración O: {self.agent2.epsilon:.2f}"
        ]
        
        y_pos = 320
        for text in stats:
            text_surface = font.render(text, True, (0, 0, 0))
            self.window.window.blit(text_surface, (10, y_pos))
            y_pos += 30
        
        pygame.display.flip()
        pygame.time.wait(200)  # Controlar velocidad de actualización

    def _get_all_lines(self, board):
        # Todas las líneas posibles (filas, columnas, diagonales)
        lines = []
        # Filas y columnas
        for i in range(3):
            lines.append([board[i][j] for j in range(3)])
            lines.append([board[j][i] for j in range(3)])
        # Diagonales
        lines.append([board[i][i] for i in range(3)])
        lines.append([board[i][2-i] for i in range(3)])
        return lines

    def _calculate_reward(self, winner: str|None, player: str, game: TicTacToeMovements) -> float:
        if winner == player:
            return 1.0
        elif winner == "Draft":
            return 0.2  # Pequeña recompensa por empate
        elif winner is not None:
            return -1.0
        
        # Recompensas intermedias por estrategia
        reward = 0.0
        board = game.board
        
        # Recompensa por crear líneas de 2
        for line in self._get_all_lines(board):
            if line.count(player) == 2 and line.count("") == 1:
                reward += 0.3
        
        # Penalizar dejar línea de 2 al oponente
        opponent = "O" if player == "X" else "X"
        for line in self._get_all_lines(board):
            if line.count(opponent) == 2 and line.count("") == 1:
                reward -= 0.4
                
        return reward

    def _update_win_stats(self, winner: str):
        if winner == "X":
            self.agent1.wins += 1
        elif winner == "O":
            self.agent2.wins += 1

    def save_best_agent(self, path: str):
        with open(path, "wb") as f:
            agent = self.agent1 if self.agent1.wins > self.agent2.wins else self.agent2
            pickle.dump(agent, f)

    @staticmethod
    def load_agent(path: str) -> QLearningAgent:
        with open(path, "rb") as f:
            return pickle.load(f)