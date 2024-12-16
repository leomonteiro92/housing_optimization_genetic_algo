import streamlit as st
import time
from utils import generate_map, plot_genetic_algorithm_score, print_individual

from model.gen_algo import GeneticAlgorithm

POPULATION_SIZE = 10
MUTATION_RATE = 0.5
MAX_GENERATIONS = 1000

model: GeneticAlgorithm = GeneticAlgorithm(POPULATION_SIZE, MUTATION_RATE)
print_individual(model.population[0])

st.write("### Score")
plot_placeholder = st.empty()

st.write("### Routes")
map_placeholder = st.empty()

for i in range(MAX_GENERATIONS):
    model.evolve()
    best_individual = model.best_solution
    best_individual_score = model.best_fitness_scores[-1]
    fig = plot_genetic_algorithm_score(
        range(len(model.best_fitness_scores)), model.best_fitness_scores
    )
    plot_placeholder.pyplot(fig)


st.success(f"Best score: {best_individual_score}")
generate_map(model.houses, model.agents, best_individual).save("map.html")
