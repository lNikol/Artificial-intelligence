import math
from connect4 import Connect4
from exceptions import AgentException




def basic_static_eval(game, my_token, opponent_token):
    if game.wins == my_token:
        return math.inf
    elif game.wins == opponent_token:
        return -math.inf
    
    my_threes = 0
    enemy_threes = 0
    for four in game.iter_fours():            
        if four.count(my_token) == 3:
            my_threes += 1
        elif four.count(opponent_token) == 3:
            enemy_threes += 1
    return my_threes - enemy_threes


def advanced_static_eval(game, my_token, opponent_token):
    if game.wins == my_token:
        return math.inf
    if game.wins == opponent_token:
        return -math.inf
        
    score = 0
    
    # Wagi dla różnych konfiguracji
    weights = {
        'four': 100,       # gotowa linia 4
        'three': 5,        # linia 3 z możliwością uzupełnienia
        'two': 2.5,        # linia 2 z możliwością uzupełnienia
        'center': 1        # kontrola środkowych kolumn
    }
    
    # Ocena środkowych kolumn
    center_count = game.center_column().count(my_token)
    score += center_count * weights['center']
    
    # Analiza wszystkich możliwych czwórek
    for four in game.iter_fours():
        my_count = four.count(my_token)
        opp_count = four.count(opponent_token)
        empty = four.count('_')
        
        if my_count == 4:
            return math.inf
        if opp_count == 4:
            return -math.inf
            
        if opp_count == 0:
            if my_count == 3 and empty == 1:
                score += weights['three']
            elif my_count == 2 and empty == 2:
                score += weights['two']
                
        if my_count == 0:
            if opp_count == 3 and empty == 1:
                score -= weights['three'] * 1.2  # większa kara za zagrożenie
            elif opp_count == 2 and empty == 2:
                score -= weights['two']
    
    return score



class AlphaBetaAgent:
    def __init__(self, my_token='o', search_depth=4, heuristic_func=basic_static_eval):
        self.heuristic_func = heuristic_func
        self.my_token = my_token
        self.opponent_token = 'x' if my_token == 'o' else 'o'
        self.search_depth = search_depth

    def decide(self, game):
        if game.who_moves != self.my_token:
            raise AgentException("Not my round")

        best_col = None
        alpha = -math.inf  # Najlepszy znany wynik dla mnie (maksymalizuję)
        beta = math.inf    # Najlepszy znany wynik dla przeciwnika (minimalizuje)
        
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
            return self.heuristic_func(game, self.my_token, self.opponent_token)

        if maximizing:
            value = -math.inf
            for col in game.possible_drops():
                new_game = self._simulate_move(game, col)
                value = max(value, self._alpha_beta(new_game, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Przycinanie beta
            return value
        else:
            value = math.inf
            for col in game.possible_drops():
                new_game = self._simulate_move(game, col)
                value = min(value, self._alpha_beta(new_game, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Przycinanie alfa
            return value

    def _basic_static_eval(self, game):
        if game.wins == self.my_token:
            return math.inf
        elif game.wins == self.opponent_token:
            return -math.inf
        
        myFours = 0
        enemyFours = 0
        for four in game.iter_fours():            
            if four.count(self.my_token) >= 3:
                myFours += 1
            elif four.count(self.opponent_token) >= 3:
                enemyFours +=1
        return myFours - enemyFours  # Remis lub gra w toku

    def _simulate_move(self, game, col):
        """Tworzy kopię gry z wykonanym ruchem"""
        new_game = Connect4(width=game.width, height=game.height)
        new_game.board = [list(row) for row in game.board]
        new_game.who_moves = game.who_moves
        new_game.game_over = game.game_over
        new_game.wins = game.wins
        new_game.drop_token(col)
        return new_game