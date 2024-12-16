import itertools
import random
import copy

from lib.population import gen_houses, gen_agents, gen_random_initial_population
from lib.metrics import fitness
from model.types import Individual, Gene


class GeneticAlgorithm:
    def __init__(
        self,
        population_size: int,
        mutation_rate: float,
        distance_weight: float = 0.25,
        date_penalty_weight: float = 0.25,
        idle_agents_penalty_weight: float = 0.25,
        uneven_visits_penalty_weight: float = 0.25,
    ):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.houses = gen_houses(25)
        self.agents = gen_agents(6)
        self.population = gen_random_initial_population(
            self.population_size, self.houses, self.agents
        )
        self.best_solution = None
        self.best_fitness_scores = []
        self.generation_counter = itertools.count(start=1)
        self.weights = (
            distance_weight,
            date_penalty_weight,
            idle_agents_penalty_weight,
            uneven_visits_penalty_weight,
        )

    def reset(self):
        self.best_solutions = []
        self.best_fitness_scores = []
        self.population = gen_random_initial_population(
            self.population_size, self.houses, self.agents
        )
        self.generation_counter = itertools.count(start=1)

    def evolve(self):
        generation = next(self.generation_counter)

        scores = [
            fitness(individual, self.agents, self.weights)
            for individual in self.population
        ]
        sorted_population = sorted(zip(self.population, scores), key=lambda x: x[1])

        (best_individual, best_individual_score) = sorted_population[0]

        self.best_solution = best_individual
        self.best_fitness_scores.append(best_individual_score)

        # Debugging
        if generation < 10 or generation % 10 == 0:
            print(f"::Generation {generation}: {best_individual_score}")

        new_population = [best_individual]

        rate = [(1 / score) if score > 0 else 0 for score in scores]
        while len(new_population) < self.population_size:
            parent1, parent2 = random.choices(self.population, weights=rate, k=2)
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)

        self.population = new_population

    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        parent1_set = set(parent1)

        parent2_set = set(parent2)
        same_genes = parent1_set.intersection(parent2_set)
        other_genes = parent1_set.union(parent2_set) - same_genes

        genes_list = list(other_genes | same_genes)
        child = []
        while len(genes_list) > 0:
            chosen_gene = random.choice(genes_list)
            child.append(chosen_gene)
            without_location = [
                gene for gene in genes_list if gene.location != chosen_gene.location
            ]
            genes_list = without_location

        return child

    def mutate(self, individual: Individual) -> Individual:
        if random.random() < self.mutation_rate:
            return individual

        n = len(individual)
        if n < 2:
            return individual

        mutated_individual = copy.deepcopy(individual)

        idx1, idx2 = random.sample(range(n), 2)
        gene1: Gene = mutated_individual[idx1]
        gene2: Gene = mutated_individual[idx2]
        gene1.agent, gene2.agent = gene2.agent, gene1.agent
        gene1.location, gene2.location = gene2.location, gene1.location

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
