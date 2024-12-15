from typing import List
from datetime import date


class Location:
    def __init__(self, lat: float, lon: float, deadline: date):
        self.lat: float = lat
        self.lon: float = lon
        self.deadline: date = deadline

    def __repr__(self):
        return f"Location(lat={self.lat}, lon={self.lon}, deadline={self.deadline})"


type Agent = str


class Gene:
    def __init__(self, agent: Agent, visit_date: date, location: Location):
        self.agent: Agent = agent
        self.visit_date: date = visit_date
        self.location: Location = location

    def __repr__(self):
        return f"Gene(agent={self.agent}, date={self.visit_date}, location={self.location})"


type Individual = List[Gene]
