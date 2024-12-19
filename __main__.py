import time
from utils import print_individual, generate_map

from model.gen_algo import GeneticAlgorithm

POPULATION_SIZE = 10
MUTATION_RATE = 0.5
MAX_GENERATIONS = 1000

model: GeneticAlgorithm = GeneticAlgorithm(POPULATION_SIZE, MUTATION_RATE)

generate_map(model.houses, model.agents, model.population[0]).save("initial_route.html")

for i in range(MAX_GENERATIONS):
    model.evolve()
    best_individual_score = model.best_fitness_scores[-1]
    time.sleep(0)

print_individual(model.best_solution)
generate_map(model.houses, model.agents, model.best_solution).save("best_route.html")
