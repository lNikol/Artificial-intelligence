from exceptions import GameplayException
from connect4 import Connect4
from randomagent import RandomAgent
from minmaxagent import MinMaxAgent, basic_static_eval, advanced_static_eval
from alphabetaagent import AlphaBetaAgent, basic_static_eval, advanced_static_eval

def run_game(agent1, agent2):
    connect4 = Connect4(width=7, height=6)
    agents = {agent1.my_token: agent1, agent2.my_token: agent2}
    while not connect4.game_over:
        #connect4.draw()
        try:
            current_agent = agents[connect4.who_moves]
            column = current_agent.decide(connect4)
            connect4.drop_token(column)
        except (ValueError, GameplayException):
            print('invalid move')
    return connect4.wins


# Testowanie basic MinMax vs Random
print("Basic MinMax (x) vs Random (o):")
for i in range(5):
    result = run_game(MinMaxAgent('x'), RandomAgent('o'))
    print(f"Game {i+1}: {'Basic MinMax wins' if result == 'x' else 'Random wins' if result == 'o' else 'Draw'}")

print("\nRandom (x) vs Basic MinMax (o):")
for i in range(5):
    result = run_game(RandomAgent('x'), MinMaxAgent('o'))
    print(f"Game {i+1}: {'Random wins' if result == 'x' else 'Basic MinMax wins' if result == 'o' else 'Draw'}")



# Testowanie advanced MinMax vs Random
print("\nAdvanced MinMax (x) vs Random (o):")
for i in range(5):
    result = run_game(MinMaxAgent('x', heuristic_func=advanced_static_eval), RandomAgent('o'))
    print(f"Game {i+1}: {'Advanced MinMax wins' if result == 'x' else 'Random wins' if result == 'o' else 'Draw'}")

print("\nRandom (x) vs Advanced MinMax (o):")
for i in range(5):
    result = run_game(RandomAgent('x'), MinMaxAgent('o', heuristic_func=advanced_static_eval))
    print(f"Game {i+1}: {'Random wins' if result == 'x' else 'Advanced MinMax wins' if result == 'o' else 'Draw'}")



# Testowanie AlphaBeta vs Random
print("\nBasic AlphaBeta (x) vs Random (o):")
for i in range(5):
    result = run_game(AlphaBetaAgent('x'), RandomAgent('o'))
    print(f"Game {i+1}: {'Basic AlphaBeta wins' if result == 'x' else 'Random wins' if result == 'o' else 'Draw'}")

print("\nRandom (x) vs AlphaBeta (o):")
for i in range(5):
    result = run_game(RandomAgent('x'), AlphaBetaAgent('o'))
    print(f"Game {i+1}: {'Random wins' if result == 'x' else 'Basic AlphaBeta wins' if result == 'o' else 'Draw'}")



# Testowanie advanced AlphaBeta vs Random
print("\nAdvanced AlphaBeta (x) vs Random (o):")
for i in range(5):
    result = run_game(AlphaBetaAgent('x', heuristic_func=advanced_static_eval), RandomAgent('o'))
    print(f"Game {i+1}: {'Advanced AlphaBeta wins' if result == 'x' else 'Random wins' if result == 'o' else 'Draw'}")

print("\nRandom (x) vs Advanced AlphaBeta (o):")
for i in range(5):
    result = run_game(RandomAgent('x'), AlphaBetaAgent('o', heuristic_func=advanced_static_eval))
    print(f"Game {i+1}: {'Random wins' if result == 'x' else 'Advanced AlphaBeta wins' if result == 'o' else 'Draw'}")



print("\n Basic AlphaBeta (x) vs Advanced AlphaBeta (o):")
for i in range(5):
    result = run_game(AlphaBetaAgent('x'), AlphaBetaAgent('o', heuristic_func=advanced_static_eval))
    print(f"Game {i+1}: {'Basic AlphaBetaAgent wins' if result == 'x' else 'Advanced AlphaBeta wins' if result == 'o' else 'Draw'}")


    
print("\n Advanced AlphaBeta (x) vs Basic AlphaBeta (o):")
for i in range(5):
    result = run_game(AlphaBetaAgent('x', heuristic_func=advanced_static_eval), AlphaBetaAgent('o'))
    print(f"Game {i+1}: {'Advanced AlphaBetaAgent wins' if result == 'x' else 'Basic AlphaBeta wins' if result == 'o' else 'Draw'}")