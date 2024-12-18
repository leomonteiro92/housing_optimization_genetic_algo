import copy
import random

from model.types import Individual, Gene


# deprecated
def v1(individual: Individual, mutation_rate: float) -> Individual:
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


def v2(individual: Individual, mutation_rate: float) -> Individual:
    mutated_individual = copy.deepcopy(individual)

    if random.random() < mutation_rate:
        n = len(individual)
        if n < 2:
            return individual

        idx1, idx2 = random.sample(range(n), 2)
        gene1: Gene = mutated_individual[idx1]
        gene2: Gene = mutated_individual[idx2]
        gene1.agent, gene2.agent = gene2.agent, gene1.agent
        gene1.location, gene2.location = gene2.location, gene1.location

        idx3, idx4 = random.sample(range(n), 2)
        gene3: Gene = mutated_individual[idx3]
        gene4: Gene = mutated_individual[idx4]
        gene3.visit_date, gene4.visit_date = gene4.visit_date, gene3.visit_date

        mutated_individual[idx1] = gene1
        mutated_individual[idx2] = gene2

    return mutated_individual
