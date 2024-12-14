import random
from datetime import date, timedelta
from typing import List
from model.types import Location, Solution, Agent, Route

# SP Zona Centro Sul
lat_min, lat_max = -23.55, -23.60
lon_min, lon_max = -46.62, -46.65
date_min, date_max = date(2024, 1, 1), date(2024, 1, 31)


def gen_houses(n: int) -> List[Location]:
    houses: List[Location] = []
    date_delta = date_max - date_min
    for _ in range(n):
        lat = random.uniform(lat_min, lat_max)
        lon = random.uniform(lon_min, lon_max)
        random_secs = random.uniform(0, date_delta.total_seconds())
        house_date = date_min + timedelta(seconds=random_secs)
        houses.append(Location(lat, lon, house_date))
    return houses


def gen_agents(n: int) -> List[Agent]:
    agents: List[Agent] = []
    for i in range(n):
        name = f"Agent {i}"
        agents.append(name)
    return agents


def _gen_random_solutions(houses: List[Location], agents: List[str]) -> List[Solution]:
    # Inicialmente vamos distribuir as casas de forma aleatória e proporcionalmente distribuídas entre os agentes
    houses_per_agent_rate: int = len(houses) // len(agents)

    # Fazemos uma copia e embaralharamos as casas
    houses_copy = houses.copy()
    random.shuffle(houses)

    result: List[Agent] = []
    for agent in agents:
        # Cada agente vai pegar um slice das casas representado por houses_per_agent_rate
        houses_for_agent = houses_copy[0:houses_per_agent_rate]

        route: List[Route] = []
        for house in houses_for_agent:
            # Para cada casa assignalada para um agente, vamos aleatóriamente selecionar uma data de visita
            date_delta = date_max - house.deadline
            random_secs = random.uniform(0, date_delta.total_seconds())
            schedule_date = date_min + timedelta(seconds=random_secs)

            route.append((schedule_date, house))
        result.append((agent, route))
        del houses_copy[0:houses_per_agent_rate]
    return result


def gen_chromossomes(
    n: int, houses: List[Location], agents: List[str]
) -> List[Solution]:
    chromossomes: List[Solution] = []
    for _ in range(n):
        chromossomes.append(_gen_random_solutions(houses, agents))
    return chromossomes
