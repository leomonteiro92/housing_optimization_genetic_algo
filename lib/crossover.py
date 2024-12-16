import random

from typing import List
from model.types import Individual, Agent, Gene


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


def _agent_genes(agents: List[Agent], parent: Individual) -> List[Gene]:
    return [gene for gene in parent if gene.agent in agents]


def v2(agents: List[str], parent1: Individual, parent2: Individual) -> Individual:
    n = len(agents)

    start_index = random.randint(0, n - 1)
    end_index = random.randint(start_index + 1, n)

    parent1_agents = agents[start_index:end_index]
    parent2_agents = [agent for agent in agents if agent not in parent1_agents]

    segment1 = _agent_genes(parent1_agents, parent1)
    segment2 = _agent_genes(parent2_agents, parent2)
    child = segment1 + segment2

    return child
