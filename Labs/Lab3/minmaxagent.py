from connect4 import Connect4
from exceptions import AgentException

class MinMaxAgent:
    def __init__(self, my_token='o', max_depth=4):
        self.my_token = my_token
        self.opponent_token = 'x' if my_token == 'o' else 'o'
        self.max_depth = max_depth

    def decide(self, game_state):
        if game_state.who_moves != self.my_token:
            raise AgentException("Not my round")

        best_move = None
        best_score = -float('inf')

        for col in game_state.possible_drops():
            temp_game = self._copy_game(game_state)
            temp_game.drop_token(col)
            
            # Rekurencyjne ocenianie ruchu
            current_score = self._minimax(temp_game, self.max_depth - 1, False)
            
            if current_score > best_score or best_move is None:
                best_score = current_score
                best_move = col

        return best_move

    def _minimax(self, game, depth, is_my_turn):
        # Warunki końca rekurencji
        if game.game_over or depth == 0:
            return self._evaluate(game)

        if is_my_turn:
            max_score = -float('inf')
            for col in game.possible_drops():
                temp_game = self._copy_game(game)
                temp_game.drop_token(col)
                score = self._minimax(temp_game, depth - 1, False)
                max_score = max(max_score, score)
            return max_score
        else:
            min_score = float('inf')
            for col in game.possible_drops():
                temp_game = self._copy_game(game)
                temp_game.drop_token(col)
                score = self._minimax(temp_game, depth - 1, True)
                min_score = min(min_score, score)
            return min_score

    def _evaluate(self, game):
        if game.wins == self.my_token:
            return 1
        elif game.wins == self.opponent_token:
            return -1
        return 0  # Remis lub gra w toku

    def _copy_game(self, game):
        """Tworzy głęboką kopię stanu gry"""
        new_game = Connect4(width=game.width, height=game.height)
        new_game.board = [row[:] for row in game.board]
        new_game.who_moves = game.who_moves
        new_game.game_over = game.game_over
        new_game.wins = game.wins
        return new_game