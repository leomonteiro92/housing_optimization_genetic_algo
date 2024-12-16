import folium
import random
import numpy as np
from typing import List
from model.types import Individual, Location, Agent
import matplotlib.pyplot as plt


def plot_genetic_algorithm_score(x, y):
    plt.close("all")
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    ax.plot(x, y)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Score")
    ax.legend()

    return fig


def _random_color():
    return "#" + "".join([random.choice("0123456789ABCDEF") for _ in range(6)])


def generate_map(
    houses: List[Location], agents: List[Agent], individual: Individual
) -> folium.Map:
    map_center = [
        np.mean([gene.location.lat for gene in individual]),
        np.mean([gene.location.lon for gene in individual]),
    ]
    m = folium.Map(location=map_center, zoom_start=14)

    for house in houses:
        folium.Marker(
            location=[house.lat, house.lon],
            popup=f"Deadline: {house.label}",
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(m)

    agentsMap = {}
    for gene in individual:
        if gene.agent not in agentsMap:
            agentsMap[gene.agent] = []
        agentsMap[gene.agent].append(gene)

    for _, agent in enumerate(agents):
        route_coords = [
            (gene.location.lat, gene.location.lon) for gene in agentsMap[agent]
        ]
        folium.PolyLine(
            route_coords,
            color=_random_color(),
            weight=4,
            opacity=0.7,
            tooltip=f"Agent: {gene.agent}",
        ).add_to(m)
    return m


def print_individual(individual: Individual):
    agentsMap = {}
    for gene in individual:
        if gene.agent not in agentsMap:
            agentsMap[gene.agent] = []
        agentsMap[gene.agent].append(gene)

    for agent, genes in agentsMap.items():
        route = [gene.location.label for gene in genes]
        print(f"Agent: {agent} - Route: {route}")
