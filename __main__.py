from lib.population import gen_houses, gen_agents, gen_chromossomes
from lib.solution import fitness

houses = gen_houses(10)
agents = gen_agents(3)

chromossomes = gen_chromossomes(10, houses, agents)

for i, chromossome in enumerate(chromossomes):
    print(f"{i}: fitness= {fitness(chromossome)}")
