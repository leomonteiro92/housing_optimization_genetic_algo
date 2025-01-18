from datetime import date, timedelta
from typing import List
import random

from model.types import Location, Individual, Agent, Gene

# SP Zona Centro Sul
lat_min, lat_max = -23.55, -23.60
lon_min, lon_max = -46.62, -46.65
date_min, date_max = date(2025, 1, 1), date(2025, 1, 31)
MIN_ADVANCED_DAYS_TIMEDELTA = timedelta(days=5)


def gen_locations(n: int) -> List[Location]:
    houses: List[Location] = []
    date_delta = date_max - date_min
    for idx in range(n):
        lat = random.uniform(lat_min, lat_max)
        lon = random.uniform(lon_min, lon_max)
        random_secs = random.uniform(0, date_delta.total_seconds())
        house_date = date_min + timedelta(seconds=random_secs)
        houses.append(Location(lat, lon, house_date, f"Location {idx}"))
    return houses


def gen_agents(n: int) -> List[Agent]:
    agents: List[Agent] = []
    for idx in range(n):
        name = f"Agent {idx}"
        agents.append(name)
    return agents


def _gen_random_individual(houses: List[Location], agents: List[str]) -> Individual:
    # Inicialmente vamos distribuir as casas de forma aleatória e proporcionalmente distribuídas entre os agentes
    houses_per_agent_rate: int = len(houses) // len(agents)
    remainder = len(houses) % len(agents)

    # Fazemos uma copia e embaralharamos as casas
    houses_copy = houses.copy()
    random.shuffle(houses)

    result: List[Gene] = []
    start = 0
    for idx in range(len(agents)):
        current_size = houses_per_agent_rate + (1 if idx < remainder else 0)
        # Cada agente vai pegar um slice das casas representado por houses_per_agent_rate
        houses_per_agent = houses_copy[start : start + current_size]
        for house in houses_per_agent:
            # Para cada casa assignalada para um agente, vamos aleatóriamente selecionar uma data de visita
            # (com um D-5 de antecedência)
            start_date = date_min - MIN_ADVANCED_DAYS_TIMEDELTA
            end_date = house.deadline - MIN_ADVANCED_DAYS_TIMEDELTA
            random_days = random.randint(0, (end_date - start_date).days)
            visit_date = start_date + timedelta(days=random_days)
            # visit_date = start_date

            result.append(
                Gene(agent=agents[idx], visit_date=visit_date, location=house)
            )
        start += current_size
    return result


def gen_random_initial_population(
    n: int, houses: List[Location], agents: List[str]
) -> List[Individual]:
    individuals: Individual = []
    for _ in range(n):
        individuals.append(_gen_random_individual(houses, agents))
    return individuals
