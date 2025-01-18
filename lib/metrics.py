import numpy as np
import pandas as pd
from typing import Tuple, List, Dict
from geopy.distance import geodesic
from dataclasses import dataclass

from model.types import Location, Individual, Gene, Agent


@dataclass
class FitnessData:
    score: float
    mean_distance: float
    mean_delta_days: float
    std_visits: float

    def as_table(self):
        return pd.DataFrame(
            {
                "Score": [self.score],
                "Distância média (km)": [self.mean_distance],
                "Média antecedência (dias)": [self.mean_delta_days],
                "Visitas por agente (σ)": [self.std_visits],
            }
        )


# Fitness retorna um score baseado na formula
# Seja w1 e w2 os pesos para melhores distâncias vs melhores datas
# score = w1 * media_das_distancias_normalizadas + w2 * (1 / (1 + media_das_datas_normalizadas))
# Por que queremos que a média de distancias seja a menor possível e
# as média de delta de dias seja a maior possível.
# Queremos penalizar os individuos que não visitam todas as
# localidades ou que deixam um agente sem nenhuma visita
def fitness(
    individual: Individual,
    agents: List[Agent],
    locations: List[Location],
    weigths: Tuple[float, float] = (0.5, 0.5),
) -> FitnessData:
    (w1, w2) = weigths

    indexed_by_agent: Dict[Agent, List[Gene]] = {}
    for gene in individual:
        if gene.agent not in indexed_by_agent:
            indexed_by_agent[gene.agent] = []
        indexed_by_agent[gene.agent].append(gene)

    if _has_penalty(individual, agents, locations):
        return FitnessData(
            score=float("inf"),
            mean_distance=float("inf"),
            mean_delta_days=float("inf"),
            std_visits=float("inf"),
        )

    mean_dist = _get_mean_distance(indexed_by_agent)
    visits_std = _get_visits_std(indexed_by_agent)
    mean_delta_days = _get_mean_delta_days(individual)

    normalized_dist = mean_dist / (mean_dist + 1e-2)
    normalized_dd = mean_delta_days / (mean_delta_days + 1e-2)

    score = w1 * normalized_dist + w2 * (1 / (1 + normalized_dd))

    return FitnessData(
        score=score,
        mean_distance=mean_dist,
        mean_delta_days=mean_delta_days,
        std_visits=visits_std,
    )


def _get_mean_delta_days(individual: Individual) -> float:
    delta_days_data = []
    for gene in individual:
        delta_days = (gene.visit_date - gene.location.deadline).days
        delta_days_data.append(abs(delta_days))
    return np.mean(delta_days_data)


def _get_mean_distance(agents_map: Dict[Agent, List[Gene]]) -> float:
    distance_data = []
    for _, agent in agents_map.items():
        distance_per_agent = 0
        for i in range(1, len(agent)):
            loc2: Location = agent[i - 1].location
            loc1: Location = agent[i].location
            distance = geodesic((loc1.lat, loc1.lon), (loc2.lat, loc2.lon)).kilometers
            distance_per_agent += distance
        distance_data.append(distance_per_agent)
    return np.mean(distance_data)


def _get_visits_std(agents_map: Dict[Agent, List[Gene]]) -> float:
    num_visits = [len(v) for _, v in agents_map.items()]
    return np.std(num_visits)


def _has_penalty(
    individual: Individual, agents: List[Agent], locations: List[Location]
) -> bool:
    agents_set = set()
    locations_set = set()
    for gene in individual:
        agents_set.add(gene.agent)
        locations_set.add(gene.location)

    return len(locations_set) != len(locations) or len(agents_set) != len(agents)
