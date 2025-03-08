from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import pickle

from app.agent.q_learning import QLearningAgent
from app.tictactoe.movements import TicTacToeMovements


@dataclass
class TrainingManager:
    agent1: QLearningAgent = field(default_factory=QLearningAgent())
    agent2: QLearningAgent = field(default_factory=QLearningAgent())
    win_rates: list[tuple[float, float]] = field(default_factory=list)

    def _get_available_actions(self, state: list[list[str]]) -> list[tuple[int, int]]:
        """Obtiene movimientos válidos desde el estado actual."""
        return [
            (r, c)
            for r in range(3)
            for c in range(3)
            if state[r][c] == ""
        ]
    
    def train_dueling_agents(self, episodes: int = 10000, save_path: str = "best_agent.pkl"):
        for episode in range(episodes):
            game = TicTacToeMovements()
            agents = {"X": self.agent1, "O": self.agent2}
            
            while True:
                current_player = "X" if game.turn % 2 == 0 else "O"
                agent = agents[current_player]
                state = [row.copy() for row in game.board]
                available = self._get_available_actions(state)
                
                if not available:
                    break
                
                # Turno del agente actual
                action = agent.choose_action(state, available)
                prev_state = [row.copy() for row in state]
                game.make_movement(*action, current_player)
                winner = game.check_winner()
                
                # Turno del oponente (simulado para aprendizaje)
                reward = self._calculate_reward(winner, current_player)
                next_state = [row.copy() for row in game.board] if not winner else None
                agent.update(prev_state, action, reward, next_state)
                
                if winner:
                    self._update_win_stats(winner)
                    break

            # Alternar agentes principal y oponente
            if episode % 100 == 0:
                self.agent1, self.agent2 = self.agent2, self.agent1
            
            # Guardar el mejor agente periódicamente
            if episode % 1000 == 0:
                self.save_best_agent(save_path)

    def _calculate_reward(self, winner: Optional[str], player: str) -> int:
        if not winner:
            return 0
        if winner == "Draft":
            return 0
        return 1 if winner == player else -1

    def _update_win_stats(self, winner: str) -> ...:
        pass

    def save_best_agent(self, path: str):
        # Comparar performance y guardar el mejor
        with open(path, "wb") as f:
            pickle.dump(self.agent1 if self.agent1.wins > self.agent2.wins else self.agent2, f)

    @staticmethod
    def load_agent(path: str) -> QLearningAgent:
        with open(path, "rb") as f:
            return pickle.load(f)