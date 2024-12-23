import folium
import random
import numpy as np
import pandas as pd
from typing import List, Tuple
from model.types import Individual, Location, Agent
import matplotlib.pyplot as plt


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


def print_individual(individual: Individual):
    agentsMap = {}
    for gene in individual:
        if gene.agent not in agentsMap:
            agentsMap[gene.agent] = []
        agentsMap[gene.agent].append(gene)

    for agent, genes in agentsMap.items():
        sorted_genes = sorted(genes, key=lambda x: x.visit_date)
        route = [f"{gene.location.label} on {gene.visit_date}" for gene in sorted_genes]
        print(f"Agent: {agent} - Route: {route}")


def get_dataframes(individual: Individual) -> Tuple[pd.DataFrame, pd.DataFrame]:
    locationsMap = {}
    agentsMap = {}
    for gene in individual:
        if gene.agent not in agentsMap:
            agentsMap[gene.agent] = {
                "total_visits": 0,
                "coords": [],
            }
        agentsMap[gene.agent]["total_visits"] += 1
        agentsMap[gene.agent]["coords"].append((gene.location.lat, gene.location.lon))

        if gene.location.label not in locationsMap:
            locationsMap[gene.location.label] = {
                "label": gene.location.label,
                "deadline": gene.location.deadline,
                "visit_date": gene.visit_date,
                "delta": abs(gene.visit_date - gene.location.deadline),
                "agent": gene.agent,
            }

    # calculate distances by agent
    for agent, data in agentsMap.items():
        total_distance = 0
        for i in range(len(data["coords"]) - 1):
            total_distance += np.linalg.norm(
                np.array(data["coords"][i]) - np.array(data["coords"][i + 1])
            )
        agentsMap[agent]["total_distance"] = total_distance
        del agentsMap[agent]["coords"]

    return (
        pd.DataFrame(locationsMap).T,
        pd.DataFrame(agentsMap).T,
    )
