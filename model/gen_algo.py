import copy
import itertools
import random

from model.metrics import fitness
from model.population import gen_locations, gen_agents, gen_random_initial_population
from model.types import Individual, Gene


class GeneticAlgorithm:
    def __init__(
        self,
        population_size: int,
        mutation_rate: float,
    ):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.locations = gen_locations(25)
        self.agents = gen_agents(6)
        self.population = gen_random_initial_population(
            self.population_size, self.locations, self.agents
        )
        self.best_solution = None
        self.best_fitness_scores = []
        self.generation_counter = itertools.count(start=1)
        self.weights = (0.5, 0.5)

    def reset(self):
        self.best_solutions = []
        self.best_fitness_scores = []
        self.population = gen_random_initial_population(
            self.population_size, self.locations, self.agents
        )
        self.generation_counter = itertools.count(start=1)

    def evolve(self):
        generation = next(self.generation_counter)

        # Seleção baseada em ranking, os melhores scores são selecionados
        scores = [
            fitness(individual, self.agents, self.locations, self.weights).score
            for individual in self.population
        ]
        sorted_population = sorted(zip(self.population, scores), key=lambda x: x[1])

        (best_individual, best_individual_score) = sorted_population[0]

        self.best_solution = best_individual
        self.best_fitness_scores.append(best_individual_score)

        # Debugging
        if generation < 10 or generation % 10 == 0:
            score = fitness(
                best_individual, self.agents, self.locations, self.weights
            ).score
            print(f"::Generation {generation}: {score}")

        new_population = [best_individual]

        rate = [(1 / score) if score > 0 else 0 for score in scores]
        while len(new_population) < self.population_size:
            parent1, parent2 = random.choices(self.population, weights=rate, k=2)
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)

        self.population = new_population

    # Scattered crossover adaptado
    # Aleatoriamente seleciona um gene de um parent ou de outro
    # Para garantir que o individuo child seja válido,
    # quando selecionamos um gene de um parent, automáticamente removemos o gene
    # que contém a location que foi selecionada (assim não resulta em uma location
    # ser visitada 2x)
    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        genes_list = list(parent1 + parent2)
        child = []
        while len(genes_list) > 0:
            chosen_gene = random.choice(genes_list)
            child.append(chosen_gene)
            genes_list = [
                gene for gene in genes_list if gene.location != chosen_gene.location
            ]
        return child

    # Swap mutation + random mutation
    # Aleatoriamente, selecionamos 2 genes e fazemos um swap do agente (swap mutation)
    # Selecionamentos alguns genes e alteramos a data de visita (random mutation)
    def mutate(self, individual: Individual) -> Individual:
        n = len(individual)

        mutated_individual = copy.deepcopy(individual)

        for _ in range(100):
            idx1, idx2 = random.sample(range(n), 2)
            gene1: Gene = mutated_individual[idx1]
            gene2: Gene = mutated_individual[idx2]
            gene1.agent, gene2.agent = gene2.agent, gene1.agent
            mutated_individual[idx1] = gene1
            mutated_individual[idx2] = gene2

            idx3, idx4 = random.sample(range(n), 2)
            gene3: Gene = mutated_individual[idx3]
            gene4: Gene = mutated_individual[idx4]
            gene3.visit_date, gene4.visit_date = gene4.visit_date, gene3.visit_date

            mutated_individual[idx3] = gene3
            mutated_individual[idx4] = gene4

            gene = random.choice(mutated_individual)
            gene.agent = random.choice(self.agents)

        return mutated_individual
