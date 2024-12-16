import numpy as np
from typing import Tuple, List, Set
from geopy.distance import geodesic

from model.types import Location, Individual, Agent

PENALTY_FACTOR = 100


def fitness(
    individual: Individual,
    agents: List[Agent],
    weigths: Tuple[float, float, float, float],
) -> float:
    (w1, w2, w3, w4) = weigths

    total_dist = _get_total_distance(individual)
    total_date_penalty = _get_total_date_penalty(individual)
    (idle_agents_penalty, uneven_visits_penalty) = _get_total_visits_penalty(
        individual, agents
    )

    return (
        w1 * total_dist
        + w2 * total_date_penalty
        + w3 * idle_agents_penalty
        + w4 * uneven_visits_penalty
    )


def _get_total_date_penalty(individual: Individual) -> float:
    penalty_data = []
    for gene in individual:
        delta_days = (gene.visit_date - gene.location.deadline).days
        if delta_days > 0:
            penalty_data.append(PENALTY_FACTOR * delta_days * 10)
        elif delta_days == 0:
            penalty_data.append(PENALTY_FACTOR / 2)
        else:
            penalty_data.append(10 / abs(delta_days))
    return np.sum(penalty_data)


def _get_total_distance(individual: Individual) -> float:
    distance_data = []
    for i in range(1, len(individual)):
        loc2: Location = individual[i - 1].location
        loc1: Location = individual[i].location
        distance = geodesic((loc1.lat, loc1.lon), (loc2.lat, loc2.lon)).kilometers
        distance_data.append(distance)
    return np.sum(distance_data)


def _get_total_visits_penalty(
    individual: Individual, agents: List[Agent]
) -> Tuple[float, float]:
    agents_per_visit_map = {}
    for gene in individual:
        if gene.agent not in agents_per_visit_map:
            agents_per_visit_map[gene.agent] = 0
        agents_per_visit_map[gene.agent] += 1

    idle_penalty = 0
    for agent in agents:
        if agent not in agents_per_visit_map:
            idle_penalty += PENALTY_FACTOR * 1000
            agents_per_visit_map[agent] = 0

    num_visits = [v for _, v in agents_per_visit_map.items()]
    std_dev = np.std(num_visits)
    uneven_penalty = std_dev * PENALTY_FACTOR
    return (idle_penalty, uneven_penalty)


def is_valid_solution(locations: List[Location], individual: Individual) -> bool:
    visited_locations: Set[Location] = set()
    for gene in individual:
        visited_locations.add(gene.location)

    return len(visited_locations) == len(locations)
