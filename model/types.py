from typing import List
from datetime import date
from dataclasses import dataclass


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
        return hash((self.agent, self.location.label))


type Individual = List[Gene]
