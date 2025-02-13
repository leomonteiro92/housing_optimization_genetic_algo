from model.gen_algo import GeneticAlgorithm

POPULATION_SIZE = 10
MUTATION_RATE = 0.5
MAX_GENERATIONS = 1000

model: GeneticAlgorithm = GeneticAlgorithm(POPULATION_SIZE, MUTATION_RATE)

for i in range(MAX_GENERATIONS):
    model.evolve()
    best_individual_score = model.best_fitness_scores[-1]
