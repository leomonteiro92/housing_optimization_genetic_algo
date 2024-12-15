import copy
import random

from model.types import Individual


def mutate(individual: Individual, mutation_rate: float) -> Individual:
    mutated_individual = copy.deepcopy(individual)

    if random.random() < mutation_rate:
        n = len(individual)
        if n < 2:
            return individual

        i, j = random.sample(range(n), 2)
        mutated_individual[i], mutated_individual[j] = (
            mutated_individual[j],
            mutated_individual[i],
        )

    return mutated_individual
