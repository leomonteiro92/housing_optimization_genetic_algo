import itertools
import numpy as np
import random

from lib.population import gen_houses, gen_agents, gen_random_initial_population
from lib.metrics import fitness
import lib.crossover as xover
import lib.mutation as mut


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
        self.houses = gen_houses(10)
        self.agents = gen_agents(3)
        self.population = gen_random_initial_population(
            self.population_size, self.houses, self.agents
        )
        print(self.population)
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
            print(f"Generation {generation}: {best_individual_score}")

        new_population = [best_individual]

        rate = [(1 / score) if score > 0 else 0 for score in scores]
        while len(new_population) < self.population_size:
            parent1, parent2 = random.choices(self.population, weights=rate, k=2)
            child = xover.OX1(parent1, parent2)
            child = mut.mutate(child, self.mutation_rate)
            new_population.append(child)

        self.population = new_population
