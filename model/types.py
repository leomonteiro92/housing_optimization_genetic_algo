from typing import Tuple, List
from datetime import date


class Location:
    def __init__(self, lat: float, lon: float, deadline: date):
        self.lat: float = lat
        self.lon: float = lon
        self.deadline: date = deadline

    def __repr__(self):
        return f"Location(lat={self.lat}, lon={self.lon}, deadline={self.deadline})"


type Route = List[(date, Location)]

type Agent = str
type Solution = Tuple[Agent, Route]
