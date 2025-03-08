from dataclasses import dataclass, field
from typing import DefaultDict
import random
from collections import defaultdict


StateKey = tuple[tuple[str, str, str], tuple[str, str, str], tuple[str, str, str]]
QKey = tuple[StateKey, tuple[int, int]]


@dataclass
class QLearningAgent:
    q_table: DefaultDict[QKey, float] = field(
        default_factory=lambda: defaultdict(float)
    )
    alpha: float = 0.7
    gamma: float = 0.95
    epsilon: float = 0.8
    wins: int = 0
    training_steps: int = 0
    exploration_decay: float = 0.9999

    def get_state_key(self, state: list[list[str]]) -> StateKey:
        """Convierte el estado en una tupla inmutable para usar como clave."""
        return tuple(tuple(row) for row in state) 

    def choose_action(
        self,
        state: list[list[str]],
        available_actions: list[tuple[int, int]],
        epsilon: float | None = None
    ) -> tuple[int, int]:
        # Decaimiento exponencial continuo (nueva implementación)
        self.training_steps += 1
        self.epsilon *= self.exploration_decay  # <-- Nueva línea clave
        self.epsilon = max(self.epsilon, 0.01)  # Mínimo de 1% de exploración
        
        epsilon = epsilon if epsilon is not None else self.epsilon  # Usar el epsilon decayendo
        
        state_key = self.get_state_key(state)
        
        if random.random() < epsilon:
            return random.choice(available_actions)
        
        q_values = {
            action: self.q_table[(state_key, action)]
            for action in available_actions
        }
        max_q = max(q_values.values())
        best_actions = [action for action, q in q_values.items() if q == max_q]
        return random.choice(best_actions)

    def update(
        self,
        state: list[list[str]],
        action: tuple[int, int],
        reward: int,
        next_state: list[list[str]]|None
    ) -> None:
        """Actualiza la Q-table usando la ecuación de Q-learning."""
        state_key = self.get_state_key(state)
        next_key = self.get_state_key(next_state) if next_state else None
        
        current_q = self.q_table[(state_key, action)]
        next_max_q = max(
            (self.q_table[(next_key, a)] for a in self._get_available_actions(next_state)),
            default=0.0
        ) if next_key else 0.0
        
        new_q = current_q + self.alpha * (reward + self.gamma * next_max_q - current_q)
        self.q_table[(state_key, action)] = new_q

        if reward == 1:
            self.wins += 1

    def _get_available_actions(self, state: list[list[str]]|None) -> list[tuple[int, int]]:
        """Lista de acciones válidas para un estado dado."""
        if not state:
            return []
        return [
            (r, c)
            for r in range(3)
            for c in range(3)
            if state[r][c] == ""
        ]
