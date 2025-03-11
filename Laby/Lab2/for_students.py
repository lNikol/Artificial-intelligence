from itertools import compress
import random
import time
import matplotlib.pyplot as plt

from data import *

def initial_population(individual_size, population_size):
    return [[random.choice([True, False]) for _ in range(individual_size)] for _ in range(population_size)]

def fitness(items, knapsack_max_capacity, individual):
    total_weight = sum(compress(items['Weight'], individual))
    if total_weight > knapsack_max_capacity:
        return 0
    return sum(compress(items['Value'], individual))

def population_best(items, knapsack_max_capacity, population):
    best_individual = None
    best_individual_fitness = -1
    # individual array with True, False for selected items
    for individual in population:
        individual_fitness = fitness(items, knapsack_max_capacity, individual)
        if individual_fitness > best_individual_fitness:
            best_individual = individual
            best_individual_fitness = individual_fitness
    return best_individual, best_individual_fitness


def sorted_population_fitnesses(items, knapsack_max_capacity, population):
    population_fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]
    population_fitnesses.sort(reverse=True)
    return population_fitnesses


def select_elite(population, items, knapsack_max_capacity, n_elite):
    # Posortuj populację według fitness (malejąco)
    sorted_population = sorted(population, key=lambda x: fitness(items, knapsack_max_capacity, x), reverse=True)
    # Wybierz n_elite najlepszych osobników
    elite = sorted_population[:n_elite]
    return elite


# select_parents 
def roulette(population, items, knapsack_max_capacity, n_selection):
    population_fitnesses = sorted_population_fitnesses(items, knapsack_max_capacity, population)
    total_fitness = sum(population_fitnesses)
    population_probabilities = []
    population_probabilities = [fitness / total_fitness for fitness in population_fitnesses]
    parent_indices = random.choices(range(len(population)), weights=population_probabilities, k=n_selection)
    # Parent selection by probability, selection of first n_selection elements
    # in parents arrays of True/False values
    parents = [population[i] for i in parent_indices]
    return parents


def tournament_pairing(parents, items, knapsack_max_capacity, tournament_size=2):
    pairs = []
    for _ in range(len(parents) // 2):
        # Select first parent
        candidates1 = random.sample(parents, tournament_size)
        parent1 = max(candidates1, key=lambda x: fitness(items, knapsack_max_capacity, x))
        
        # Select second parent
        candidates2 = random.sample(parents, tournament_size)
        parent2 = max(candidates2, key=lambda x: fitness(items, knapsack_max_capacity, x))
        
        pairs.append((parent1, parent2))
    return pairs


# Items selecting for children
def xover(parent1, parent2):
    child1 = []
    child2 = []
    for i in range(len(parent1)):
        if random.random() < 0.5: 
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])
    return child1, child2

# uniform crossover
def crossover(parents, items, knapsack_max_capacity, population_size):
    pairs = tournament_pairing(parents, items, knapsack_max_capacity)
    offspring = []
    for parent1, parent2 in pairs:
        child1, child2 = xover(parent1, parent2)
        offspring.extend([child1, child2])
    return offspring[:population_size]


# Changing True/False on False/True with probability mutation_rate (in %)
def mutate_individual(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = not individual[i] 
    return individual

def mutate(population, mutation_rate=0.05):
    return [mutate_individual(individual, mutation_rate) for individual in population]

items, knapsack_max_capacity = get_small()
print(items)

population_size = 100
generations = 200
n_selection = 20
n_elite = 1

start_time = time.time()
best_solution = None
best_fitness = 0
population_history = []
best_history = []
population = initial_population(len(items), population_size)

for _ in range(generations):
    population_history.append(population)

    elite = select_elite(population, items, knapsack_max_capacity, n_elite)

    parents = roulette(population, items, knapsack_max_capacity, n_selection)

    offspring = crossover(parents, items, knapsack_max_capacity, population_size - n_elite)

    mutated_offspring = mutate(offspring)

    # Adding elite on the beggining of population
    # and adding mutated_offspring after elite in this population
    population = elite + mutated_offspring  

    # Aktualizacja najlepszego rozwiązania
    best_individual, best_individual_fitness = population_best(items, knapsack_max_capacity, population)
    if best_individual_fitness > best_fitness:
        best_solution = best_individual
        best_fitness = best_individual_fitness
    best_history.append(best_fitness)



end_time = time.time()
total_time = end_time - start_time
print('Best solution:', list(compress(items['Name'], best_solution)))
print('Best solution value:', best_fitness)
print('Time: ', total_time)

# plot generations
x = []
y = []
top_best = 10
for i, population in enumerate(population_history):
    plotted_individuals = min(len(population), top_best)
    x.extend([i] * plotted_individuals)
    # this line: [fitness(items, knapsack_max_capacity, individual) for individual in population]
    # adds to population_fitnesses in place by id [population_fitnesses] value from fitness()
    # extends population_fitnesses with fitness() values
    population_fitnesses = sorted_population_fitnesses(items, knapsack_max_capacity, population)
    y.extend(population_fitnesses[:plotted_individuals])
plt.scatter(x, y, marker='.')
plt.plot(best_history, 'r')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()
