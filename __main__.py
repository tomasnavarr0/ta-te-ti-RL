from app.agent.training_manager import TrainingManager
from app.agent.q_learning import QLearningAgent
import pygame
import sys
import os
from app.tictactoe.movements import TicTacToeMovements
from app.pygame.window import Window

def main():
    # Configuración inicial
    window = Window()
    MODEL_PATH = "best_agent.pkl"
    
    # Modo de operación (cambiar según necesidad)
    TRAINING_MODE = True  # True para ver entrenamiento, False para jugar
    VISUALIZE_TRAINING = True  # Mostrar entrenamiento en tiempo real
    
    if TRAINING_MODE:
        if os.path.exists(MODEL_PATH):
            best_agent = TrainingManager.load_agent(MODEL_PATH)
        else:
            agent1 = QLearningAgent(alpha=0.3, gamma=0.9, epsilon=0.2)
            agent2 = QLearningAgent(alpha=0.3, gamma=0.9, epsilon=0.2)
            
            # Entrenar con visualización
            trainer = TrainingManager(agent1, agent2, visualize=VISUALIZE_TRAINING)
            trainer.train_dueling_agents(episodes=2000, save_path=MODEL_PATH)  # Reducir episodios para demo
            
            best_agent = TrainingManager.load_agent(MODEL_PATH)
        
        if VISUALIZE_TRAINING:
            # Mantener ventana abierta después de entrenar
            while True:
                window.window.fill((255,255,255))
                window.draw_table([[None]*3 for _ in range(3)])
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    # Configurar juego humano vs IA
    player_scores = {"X": 0, "O": 0}
    first_player = "X"
    HUMAN_PLAYER = "X"
    AI_PLAYER = "O"

    while True:
        board = TicTacToeMovements()
        current_player = first_player
        game_active = True

        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Turno humano
                if current_player == HUMAN_PLAYER and event.type == pygame.MOUSEBUTTONDOWN:
                    row, col = window.get_cell(event.pos)
                    if board.make_movement(row, col, HUMAN_PLAYER):
                        winner = board.check_winner()
                        if winner:
                            _handle_game_end(winner, player_scores)
                            game_active = False
                        current_player = AI_PLAYER

            # Turno de la IA
            if game_active and current_player == AI_PLAYER:
                state = board.board
                available_moves = [(r, c) for r in range(3) for c in range(3) if state[r][c] == ""]
                
                if available_moves:
                    action = best_agent.choose_action(state, available_moves, epsilon=0)
                    board.make_movement(*action, AI_PLAYER)
                    winner = board.check_winner()
                    if winner:
                        _handle_game_end(winner, player_scores)
                        game_active = False
                    current_player = HUMAN_PLAYER

            window.draw_table(board.board)
        
        # Alternar primer jugador para la próxima partida
        first_player = AI_PLAYER if first_player == HUMAN_PLAYER else HUMAN_PLAYER

def _handle_game_end(winner: str, scores: dict):
    if winner == "Draft":
        print("¡Es un empate!")
    else:
        print(f"¡{winner} ha ganado!")
        scores[winner] += 1
    print(f"Puntuaciones: X = {scores['X']}, O = {scores['O']}")

if __name__ == "__main__":
    main()