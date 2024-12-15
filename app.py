import matplotlib.pyplot as plt
import streamlit as st
import time

from model.gen_algo import GeneticAlgorithm

POPULATION_SIZE = 10
MUTATION_RATE = 0.5
MAX_GENERATIONS = 100

model: GeneticAlgorithm = GeneticAlgorithm(POPULATION_SIZE, MUTATION_RATE)


def plot_score(x, y):
    plt.close("all")
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    ax.plot(x, y)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Score")
    ax.legend()

    return fig


st.write("### Score")
plot_placeholder = st.empty()

st.write("### Routes")
map_placeholder = st.empty()

for i in range(MAX_GENERATIONS):
    model.evolve()
    best_individual = model.best_solution
    best_individual_score = model.best_fitness_scores[-1]
    fig = plot_score(range(len(model.best_fitness_scores)), model.best_fitness_scores)
    plot_placeholder.pyplot(fig)

    # time.sleep(0.5)

st.success(f"Best score: {best_individual}")
