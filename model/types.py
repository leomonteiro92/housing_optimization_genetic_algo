from typing import List
from datetime import date
from dataclasses import dataclass


@dataclass
class Location:
    lat: float
    lon: float
    deadline: date
    label: str


type Agent = str


@dataclass
class Gene:
    agent: Agent
    visit_date: date
    location: Location


type Individual = List[Gene]
