import time
import streamlit as st
from streamlit_folium import folium_static

from utils import generate_map, plot_genetic_algorithm_score
from model.gen_algo import GeneticAlgorithm

st.set_page_config(
    layout="wide",
    page_title="Genetic Algorithm",
)


def play() -> float:
    POPULATION_SIZE = 10
    MUTATION_RATE = 0.8
    MAX_GENERATIONS = 1000
    model: GeneticAlgorithm = GeneticAlgorithm(POPULATION_SIZE, MUTATION_RATE)
    for _ in range(MAX_GENERATIONS):
        model.evolve()
        best_individual = model.best_solution
        best_individual_score = model.best_fitness_scores[-1]
        fig = plot_genetic_algorithm_score(
            range(len(model.best_fitness_scores)), model.best_fitness_scores
        )
        plot_placeholder.pyplot(fig)
        with map_placeholder:
            m = generate_map(model.houses, model.agents, best_individual)
            folium_static(m)
        time.sleep(0)
    return best_individual_score


# two columns
col1, col2 = st.columns(2)

with col1:
    col1.write("### Gerações vs Scores")
    plot_placeholder = col1.empty()

with col2:
    col2.write("### Melhores rotas")
    map_placeholder = col2.empty()

best_individual_score = play()
st.success(f"Best score: {best_individual_score}")
