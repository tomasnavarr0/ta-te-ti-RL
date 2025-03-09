from dataclasses import dataclass, field
from typing import DefaultDict
import random
from collections import defaultdict


StateKey = tuple[tuple[str, str, str], tuple[str, str, str], tuple[str, str, str]]
QKey = tuple[StateKey, tuple[int, int]]


@dataclass
class QLearningAgent:
    name: str 
    q_table: DefaultDict[QKey, float] = field(default_factory=lambda: defaultdict(float))
    alpha: float = 0.8
    gamma: float = 0.90
    epsilon: float = 0.5
    wins: float = 0
    training_steps: int = 0
    exploration_decay: float = 0.9995
    

    def get_state_key(self, state: list[list[str]]) -> StateKey:
        return tuple(tuple(row) for row in state)

    def choose_action(
        self,
        state: list[list[str]],
        available_actions: list[tuple[int, int]],
        epsilon: float | None = None
    ) -> tuple[int, int]:
        self.training_steps += 1
        self.epsilon = max(0.01, self.epsilon * self.exploration_decay)
        epsilon = epsilon or self.epsilon
        
        state_key = self.get_state_key(state)
        
        if random.random() < epsilon:
            return random.choice(available_actions)
        
        q_values = {action: self.q_table[(state_key, action)] for action in available_actions}
        max_q = max(q_values.values())
        best_actions = [action for action, q in q_values.items() if q == max_q]
        return random.choice(best_actions)

    def update(
        self,
        state: list[list[str]],
        action: tuple[int, int],
        reward: float,
        next_state: list[list[str]] | None
    ) -> None:
        """Actualización con mirror learning para generalización simétrica"""
        # Aprendizaje normal
        self._q_learning_update(state, action, reward, next_state)
        
        # Aprendizaje con estado espejo
        if state and next_state:  # Solo si hay estados válidos
            mirrored_state = self._mirror_state(state)
            mirrored_action = self._mirror_action(action)
            mirrored_next = self._mirror_state(next_state)
            self._q_learning_update(mirrored_state, mirrored_action, reward, mirrored_next)

        if reward == 1:
            self.wins += 1

    def _q_learning_update(
        self,
        state: list[list[str]],
        action: tuple[int, int],
        reward: float,
        next_state: list[list[str]] | None
    ):
        state_key = self.get_state_key(state)
        next_key = self.get_state_key(next_state) if next_state else None
        
        current_q = self.q_table.get((state_key, action), 0)
        
        # Corregir cálculo de next_max_q
        next_max_q = 0
        if next_key:
            available_actions = self._get_available_actions(next_state)
            if available_actions:
                next_max_q = max(
                    self.q_table.get((next_key, a), 0) 
                    for a in available_actions
                )
        
        new_q = current_q + self.alpha * (reward + self.gamma * next_max_q - current_q)
        self.q_table[(state_key, action)] = new_q

    def _mirror_state(self, state: list[list[str]] | None) -> list[list[str]] | None:
        """Crea una versión espejo (rotación 180°) del estado"""
        if not state:
            return None
        return [row[::-1] for row in reversed(state)]

    def _mirror_action(self, action: tuple[int, int]) -> tuple[int, int]:
        """Ajusta la acción para el estado espejo"""
        return (2 - action[0], 2 - action[1])

    def _get_available_actions(self, state: list[list[str]] | None) -> list[tuple[int, int]]:
        if not state:
            return []
        return [(r, c) for r in range(3) for c in range(3) if state[r][c] == ""]