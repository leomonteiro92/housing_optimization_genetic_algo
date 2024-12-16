import random

from typing import List, Tuple
from model.types import Individual, Agent, Gene


# deprecated
def v1(parent1: Individual, parent2: Individual) -> Individual:
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


def v3(parent1: Individual, parent2: Individual) -> Individual:
    # combine genes that share the same agent and same location
    parent1_set = set(parent1)
    parent2_set = set(parent2)
    same_genes = parent1_set.intersection(parent2_set)
    other_genes = parent1_set.union(parent2_set) - same_genes

    genes_list = list(other_genes)
    child = []
    while len(genes_list) > 0:
        chosen_gene = random.choice(genes_list)
        child.append(chosen_gene)
        without_location = [
            gene for gene in genes_list if gene.location != chosen_gene.location
        ]
        genes_list = without_location

    return parent1
