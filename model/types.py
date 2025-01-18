from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class Location:
    lat: float
    lon: float
    deadline: date
    label: str

    def __hash__(self):
        return hash((self.label, self.lat, self.lon))


type Agent = str


@dataclass
class Gene:
    agent: Agent
    visit_date: date
    location: Location

    def __hash__(self):
        return hash((self.agent, self.location.label, self.visit_date))


type Individual = List[Gene]
