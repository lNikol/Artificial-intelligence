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

class MinMaxAgent:
    def __init__(self, my_token='o', max_depth=4, heuristic_func=basic_static_eval):
        self.heuristic_func = heuristic_func
        self.my_token = my_token
        self.opponent_token = 'x' if my_token == 'o' else 'o'
        self.max_depth = max_depth

    def decide(self, game_state):
        if game_state.who_moves != self.my_token:
            raise AgentException("Not my round")

        best_move = None
        best_score = -math.inf

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
            return self.heuristic_func(game, self.my_token, self.opponent_token)

        if is_my_turn: # maksymalizacja
            max_score = -math.inf
            for col in game.possible_drops():
                temp_game = self._copy_game(game)
                temp_game.drop_token(col)
                score = self._minimax(temp_game, depth - 1, False)
                max_score = max(max_score, score)
            return max_score
        else:
            min_score = math.inf # minimalizacja
            for col in game.possible_drops():
                temp_game = self._copy_game(game)
                temp_game.drop_token(col)
                score = self._minimax(temp_game, depth - 1, True)

                min_score = min(min_score, score)
            return min_score

    def _copy_game(self, game):
        """Tworzy głęboką kopię stanu gry"""
        new_game = Connect4(width=game.width, height=game.height)
        new_game.board = [row[:] for row in game.board]
        new_game.who_moves = game.who_moves
        new_game.game_over = game.game_over
        new_game.wins = game.wins
        return new_game