from typing import List
import folium
import matplotlib.pyplot as plt
import numpy as np

from model.types import Individual, Location, Agent


def plot_genetic_algorithm_score(x, y):
    plt.close("all")
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    ax.plot(x, y)
    ax.set_xlabel("Geração")
    ax.set_ylabel("Score")
    ax.legend()
    fig.tight_layout()

    return fig


colors = [
    "red",
    "blue",
    "green",
    "purple",
    "orange",
    "darkred",
    "lightred",
    "beige",
    "darkblue",
    "darkgreen",
    "cadetblue",
    "darkpurple",
]


def generate_map(
    houses: List[Location], agents: List[Agent], individual: Individual
) -> folium.Map:
    map_center = [
        np.mean([gene.location.lat for gene in individual]),
        np.mean([gene.location.lon for gene in individual]),
    ]
    m = folium.Map(location=map_center, zoom_start=13)

    for house in houses:
        folium.CircleMarker(
            location=[house.lat, house.lon],
            radius=5,
            popup=f"Deadline: {house.label}",
            color="black",
            fill=False,
            fill_color="transparent",
            fill_opacity=0.7,
        ).add_to(m)

    agentsMap = {}
    for gene in individual:
        if gene.agent not in agentsMap:
            agentsMap[gene.agent] = []
        agentsMap[gene.agent].append(gene)

    for i, agent in enumerate(agents):
        route_coords = [
            (gene.location.lat, gene.location.lon) for gene in agentsMap[agent]
        ]
        folium.PolyLine(
            route_coords,
            color=colors[i % len(colors)],
            weight=4,
            opacity=0.7,
            tooltip=f"Agent: {agent}",
        ).add_to(m)
    return m
