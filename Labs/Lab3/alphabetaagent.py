from connect4 import Connect4
from exceptions import AgentException

class AlphaBetaAgent:
    def __init__(self, my_token='o', search_depth=4):
        self.me = my_token
        self.opponent = 'x' if my_token == 'o' else 'o'
        self.search_depth = search_depth

    def decide(self, game):
        if game.who_moves != self.me:
            raise AgentException("Not my round")

        best_col = None
        alpha = -float('inf')  # Najlepszy znany wynik dla mnie (maksymalizuję)
        beta = float('inf')    # Najlepszy znany wynik dla przeciwnika (minimalizuje)

        for column in game.possible_drops():
            simulated_game = self._simulate_move(game, column)
            
            move_score = self._alpha_beta(
                simulated_game, 
                self.search_depth - 1, 
                alpha, 
                beta, 
                maximizing=False
            )

            # Aktualizacja najlepszego ruchu
            if move_score > alpha or best_col is None:
                alpha = move_score
                best_col = column

        return best_col

    def _alpha_beta(self, game, depth, alpha, beta, maximizing):
        # Warunki końca rekurencji
        if game.game_over or depth <= 0:
            return self._score_position(game)

        if maximizing:
            value = -float('inf')
            for col in game.possible_drops():
                new_game = self._simulate_move(game, col)
                value = max(value, self._alpha_beta(new_game, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Przycinanie beta
            return value
        else:
            value = float('inf')
            for col in game.possible_drops():
                new_game = self._simulate_move(game, col)
                value = min(value, self._alpha_beta(new_game, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Przycinanie alfa
            return value

    def _score_position(self, game):
        """Prosta funkcja oceniająca pozycję"""
        if game.wins == self.me:
            return 1
        if game.wins == self.opponent:
            return -1
        return 0

    def _simulate_move(self, game, col):
        """Tworzy kopię gry z wykonanym ruchem"""
        new_game = Connect4(width=game.width, height=game.height)
        new_game.board = [list(row) for row in game.board]
        new_game.who_moves = game.who_moves
        new_game.game_over = game.game_over
        new_game.wins = game.wins
        new_game.drop_token(col)
        return new_game