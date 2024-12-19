import numpy as np
from typing import Tuple, List, Set, Dict
from geopy.distance import geodesic

from model.types import Location, Individual, Gene, Agent

PENALTY_FACTOR = 100


def fitness(
    individual: Individual,
    agents: List[Agent],
    weigths: Tuple[float, float, float, float],
) -> float:
    (w1, w2, w3, w4) = weigths

    agents_visit_map: Dict[Agent, List[Gene]] = {}
    for gene in individual:
        if gene.agent not in agents_visit_map:
            agents_visit_map[gene.agent] = []
        agents_visit_map[gene.agent].append(gene)

    mean_dist = _get_mean_distance(agents_visit_map)
    total_date_penalty = _get_total_date_penalty(individual)
    (idle_agents_penalty, uneven_visits_penalty) = _get_total_visits_penalty(
        agents_visit_map, agents
    )

    return (
        w1 * mean_dist
        + w2 * total_date_penalty
        + w3 * idle_agents_penalty
        + w4 * uneven_visits_penalty
    )


def fitness_data(
    individual: Individual,
    agents: List[Agent],
) -> Tuple[float, float, float, float]:

    agents_visit_map: Dict[Agent, List[Gene]] = {}
    for gene in individual:
        if gene.agent not in agents_visit_map:
            agents_visit_map[gene.agent] = []
        agents_visit_map[gene.agent].append(gene)

    mean_dist = _get_mean_distance(agents_visit_map)
    total_date_penalty = _get_total_date_penalty(individual)
    (idle_agents_penalty, uneven_visits_penalty) = _get_total_visits_penalty(
        agents_visit_map, agents
    )

    return (mean_dist, total_date_penalty, idle_agents_penalty, uneven_visits_penalty)


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
    return np.mean(penalty_data)


def _get_total_distance(individual: Individual) -> float:
    distance_data = []
    for i in range(1, len(individual)):
        loc2: Location = individual[i - 1].location
        loc1: Location = individual[i].location
        distance = geodesic((loc1.lat, loc1.lon), (loc2.lat, loc2.lon)).kilometers
        distance_data.append(distance)
    return np.sum(distance_data)


def _get_mean_distance(agents_map: Dict[Agent, List[Gene]]) -> float:
    distance_data = []
    for _, genes in agents_map.items():
        distance_per_agent = 0
        for i in range(1, len(genes)):
            loc2: Location = genes[i - 1].location
            loc1: Location = genes[i].location
            distance = geodesic((loc1.lat, loc1.lon), (loc2.lat, loc2.lon)).kilometers
            distance_per_agent += distance
        distance_data.append(distance_per_agent)
    return np.max(distance_data)


def _get_total_visits_penalty(
    agents_map: Dict[Agent, List[Gene]], agents: List[Agent]
) -> Tuple[float, float]:
    idle_penalty = 0
    for agent in agents:
        if agent not in agents_map:
            idle_penalty += PENALTY_FACTOR * 1000

    num_visits = [len(v) for _, v in agents_map.items()]
    return (idle_penalty, np.std(num_visits))


def is_valid_solution(locations: List[Location], individual: Individual) -> bool:
    visited_locations: Set[Location] = set()
    for gene in individual:
        visited_locations.add(gene.location)

    return len(visited_locations) == len(locations)
