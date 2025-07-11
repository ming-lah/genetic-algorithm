import random
from utils import fitness, distance_cites, population_diversity
from init_population import init_populations
from selections import tournament_selcetion, selection
from crossover import order_crossover, pmx_crossover
from mutate import mutate_swap, two_opt, two_opt_limited, disturb_path
import time

def run_ga(dist_matrix, 
           pop_size=300, 
           generations=2000, 
           crossover_rate=0.9, 
           mutation_rate=0.05, 
           elitism_count=3,
           gen_two_opt=200,
           use_two_opt=False,
           two_opt_strategy='Normal',
           init_strategy='random',
           selection_strategy='tournament',
           crossover_strategy='order',
           early_stop=500):
    num_cities = len(dist_matrix)

    best_distance_gen = []
    avg_distance_gen = []

    if init_strategy == 'random':
        population = init_populations(pop_size, num_cities, dist_matrix, 'random')
    elif init_strategy == 'nearest':
        population = init_populations(pop_size, num_cities, dist_matrix, 'nearest')
    elif init_strategy == 'mixed':
        population = init_populations(pop_size, num_cities, dist_matrix, 'mixed')

    best_individual = None
    best_fit = float('-inf')
    last_improven_gen = 0
    original_mutation = mutation_rate

    for gen in range(generations):

        if selection_strategy == 'tournament':
            population = tournament_selcetion(population, dist_matrix)
        else:
            population = selection(population, dist_matrix)

        sorted_pop = sorted(population, key=lambda ind: fitness(dist_matrix, ind), reverse=True)
        elties = [ind[:] for ind in sorted_pop[:elitism_count]] if elitism_count > 0 else []

        current_best = sorted_pop[0]
        current_best_fit = fitness(dist_matrix, current_best)
        if current_best_fit > best_fit:
            best_individual = current_best[:]
            best_fit = current_best_fit
            last_improven_gen = gen
            mutation_rate = original_mutation
        elif gen - last_improven_gen > early_stop // 4:
            disturbed = disturb_path(best_individual, strength=0.3)
            repaired = two_opt_limited(disturbed, dist_matrix, max_swaps=3)
            if fitness(dist_matrix, repaired) > fitness(dist_matrix, best_individual):
                best_individual = repaired
                last_improven_gen = gen
        elif gen - last_improven_gen > early_stop // 2:
            mutation_rate = original_mutation * 3

        diversity = population_diversity(population)
        if diversity < 0.1:
            mutation_rate = original_mutation * 3
            replace_count = max(5, int(0.05 * len(population)))
            for i in range(replace_count):
                population[-(i+1)] = random.sample(range(num_cities), num_cities)
        else:
            mutation_rate = original_mutation



        next_population = elties[:]

        while len(next_population) < pop_size:
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            if random.random() < crossover_rate:
                if crossover_strategy == 'order':
                    child1, child2 = order_crossover(parent1, parent2)
                elif crossover_strategy == 'pmx':
                    child1, child2 = pmx_crossover(parent1, parent2)
                elif crossover_strategy == 'mixed':
                    if random.random() < 0.5:
                        child1, child2 = order_crossover(parent1, parent2)
                    else:
                        child1, child2 = pmx_crossover(parent1, parent2)
                else:
                    child1, child2 = parent1[:], parent2[:]
            else:
                child1, child2 = parent1[:], parent2[:]

            mutate_swap(child1, mutation_rate)
            mutate_swap(child2, mutation_rate)
            next_population.append(child1)
            if len(next_population) < pop_size:
                next_population.append(child2)

        if gen % gen_two_opt == 0 and use_two_opt:
            if two_opt_strategy == 'normal':
                top_k = int(0.01 * len(next_population))
                for i in range(top_k):
                    next_population[i] = two_opt(next_population[i], dist_matrix)
            elif two_opt_strategy == 'limited':
                best_individual = two_opt_limited(best_individual, dist_matrix, max_swaps=2)

        population = next_population

        
        avg_fit = sum(fitness(dist_matrix, ind) for ind in population) / len(population)
        avg_dist = 1.0 / avg_fit

        best_distance_gen.append(1.0 / best_fit)
        avg_distance_gen.append(avg_dist)

        if gen % 100 == 0:
            fits = [fitness(dist_matrix, ind) for ind in population]
            avg_fit = sum(fits) / len(fits)
            print(f"第{gen}代：最佳长度 {1.0 / best_fit:.2f}，平均长度 {1.0 / avg_fit:.2f}")
        

        if gen - last_improven_gen >= early_stop:
            print("提前终止!")
            break
    return best_individual, 1.0 / best_fit, best_distance_gen, avg_distance_gen


def run_ga_on_cities(cities, 
                     pop_size=300,  
                     generations=2000, 
                     crossover_rate=0.9, 
                     mutation_rate=0.05, 
                     elitism_count=3,
                     gen_two_opt=200,
                     use_two_opt=False,
                     two_opt_strategy='limited',
                     init_strategy='random',
                     selection_strategy='tournament',
                     crossover_strategy='order',
                     early_stop=500):
    dist_matrix = distance_cites(cities)
    return run_ga(dist_matrix, pop_size, generations, crossover_rate, mutation_rate, elitism_count, gen_two_opt, use_two_opt, two_opt_strategy, init_strategy, selection_strategy, crossover_strategy,early_stop)
