
import random
from app.tictactoe.movements import TicTacToeMovements
from .q_learning import QLearningAgent


def train_agent(agent: QLearningAgent, episodes: int = 10000) -> None:
    """Entrena al agente jugando contra un oponente aleatorio."""
    for _ in range(episodes):
        game = TicTacToeMovements()
        state: list[list[str]] = game.board.copy()
        game_over = False
        
        while not game_over:
            available_actions = agent._get_available_actions(state)
            if not available_actions:
                break
            
            action = agent.choose_action(state, available_actions)
            prev_state: list[list[str]] = [row.copy() for row in state]
            
            game.make_movement(*action, "O")
            winner: str|None = game.check_winner()
            
            if winner == "O":
                reward = 1
                next_state = None
                game_over = True
            elif winner == "Draft":
                reward = 0
                next_state = None
                game_over = True
            else:
                available_opponent = agent._get_available_actions(game.board)
                if not available_opponent:
                    break
                
                opponent_action: tuple[int, int] = random.choice(available_opponent)
                game.make_movement(*opponent_action, "X")
                winner = game.check_winner()
                
                if winner == "X":
                    reward = -1
                    next_state = None
                    game_over = True
                elif winner == "Draft":
                    reward = 0
                    next_state = None
                    game_over = True
                else:
                    reward = 0
                    next_state = [row.copy() for row in game.board]
                    game_over = False
            
            agent.update(prev_state, action, reward, next_state)
            state = next_state if next_state else None