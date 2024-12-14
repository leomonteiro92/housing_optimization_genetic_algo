from model.types import Solution, Route, Location
from typing import List
import numpy as np
from geopy.distance import geodesic


def fitness(solutions: List[Solution]) -> float:
    weigh1, weigh2 = 0.5, 0.5
    fitness_data = []

    for solution in solutions:
        total_dist = _get_total_distance(solution)
        total_date_penalty = _get_total_date_penalty(solution)

        fitness_data.append(weigh1 * total_dist + weigh2 * total_date_penalty)

    return np.sum(fitness_data)


def _get_total_date_penalty(solution: Solution) -> float:
    routes: Route = solution[1]
    penalty_data = []
    for schedule_date, location in routes:
        penalty = (schedule_date - location.deadline).days
        penalty_data.append(abs(penalty))
    return np.sum(penalty_data)


def _get_total_distance(solution: Solution) -> float:
    routes: Route = solution[1]
    distance_data = []
    for i in range(1, len(routes)):
        loc2: Location = routes[i - 1][1]
        loc1: Location = routes[i][1]
        distance = geodesic((loc1.lat, loc1.lon), (loc2.lat, loc2.lon)).kilometers
        distance_data.append(distance)
    return np.sum(distance_data)
