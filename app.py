import time
import streamlit as st
from streamlit_folium import folium_static

from utils import generate_map, plot_genetic_algorithm_score
from model.gen_algo import GeneticAlgorithm

st.set_page_config(
    layout="wide",
    page_title="Genetic Algorithm",
)

model: GeneticAlgorithm = GeneticAlgorithm(10, 0.8)


if "play" not in st.session_state:
    st.session_state.play = False
if "pause" not in st.session_state:
    st.session_state.pause = False
if "reset" not in st.session_state:
    st.session_state.reset = False


def handle_play():
    st.session_state.play = True
    st.session_state.pause = False
    st.session_state.reset = False
    model: GeneticAlgorithm = GeneticAlgorithm(population_size, mutation_rate)


def handle_pause():
    st.session_state.play = False
    st.session_state.pause = True


def handle_reset():
    st.session_state.play = False
    st.session_state.pause = False
    st.session_state.reset = True


st.sidebar.subheader("Controles")
col_play, col_pause, col_reset = st.sidebar.columns(3)
with col_play:
    st.button("▶️ Play", on_click=handle_play)
with col_pause:
    st.button("⏸️ Pause", on_click=handle_pause)
with col_reset:
    st.button("🔄 Reset", on_click=handle_reset)

st.sidebar.subheader("Configurações")
population_size = st.sidebar.slider("Tamanho da população", 10, 50, 10)
mutation_rate = st.sidebar.slider("Taxa de mutação", 0.1, 1.0, 0.8)
max_generations = st.sidebar.slider("Número de gerações", 100, 1000, 1000)

st.sidebar.subheader("Pesos")
weights = st.sidebar.slider(
    "Menor distância ⬅️ | ➡️ Melhores datas",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01,
)
w1 = 1.0 - weights
w2 = weights
st.sidebar.write(f"Menor distância: {w1:.2f}% | Melhores datas: {w2:.2f}%")

st.sidebar.subheader("Constraints")
st.sidebar.checkbox("Não permitir agentes sem visitas", value=True, disabled=True)
st.sidebar.checkbox("Balancear visitas entre os agentes", value=True, disabled=True)

# two columns
col1, col2 = st.columns(2)

with col1:
    col1.write("### Gerações vs Scores")
    plot_placeholder = col1.empty()

with col2:
    col2.write("### Rota inicial")
    map1_placeholder = col2.empty()
    col2.write("### Melhor rota")
    map2_placeholder = col2.empty()


def run_generations(model: GeneticAlgorithm, max_generations: int) -> float:
    for _ in range(max_generations):
        model.evolve()
        time.sleep(0)

        best_individual_score = model.best_fitness_scores[-1]
        fig = plot_genetic_algorithm_score(
            range(len(model.best_fitness_scores)), model.best_fitness_scores
        )
        plot_placeholder.pyplot(fig)
        with map2_placeholder:
            m2 = generate_map(model.houses, model.agents, model.best_solution)
            folium_static(m2)
    return best_individual_score


with map1_placeholder:
    m1 = generate_map(model.houses, model.agents, model.population[0])
    folium_static(m1)
with map1_placeholder:
    st.spinner("Calculando melhor rota...")
run_generations(model, max_generations)
