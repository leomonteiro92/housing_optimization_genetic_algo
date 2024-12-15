import random

from model.types import Individual


def OX1(parent1: Individual, parent2: Individual) -> Individual:
    n = len(parent1)

    start_index = random.randint(0, n - 1)
    end_index = random.randint(start_index + 1, n)

    child = parent1[start_index:end_index]

    remaining_positions = [
        i for i in range(n) if i not in range(start_index, end_index)
    ]

    remaining_genes = [gene for gene in parent2 if gene not in child]

    for pos, gene in zip(remaining_positions, remaining_genes):
        child.insert(pos, gene)

    return child
