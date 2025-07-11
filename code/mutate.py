import random
from utils import get_total


def mutate_swap(individual, mutation_rate=0.005) -> None:
    """
    交换变异
    """
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]

def two_opt(route, dist_matrix):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue
                new_route = route[:]
                new_route[i:j] = route[j-1:i-1:-1]
                if get_total(dist_matrix, new_route) < get_total(dist_matrix, best):
                    best = new_route
                    improved = True
        route = best
    return best


def two_opt_limited(route, dist_matrix, max_swaps=2):
    best = route[:]
    best_dist = get_total(dist_matrix, best)
    count = 0
    n = len(route)

    for i in range(1, n - 2):
        for j in range(i + 1, n):
            if j - i == 1:
                continue
            new_route = best[:]
            new_route[i:j] = reversed(new_route[i:j])
            new_dist = get_total(dist_matrix, new_route)
            if new_dist < best_dist:
                best = new_route
                best_dist = new_dist
                count += 1
                if count >= max_swaps:
                    return best
    return best

def disturb_path(path, strength=0.2):
    path = path[:]
    n = len(path)
    for _ in range(int(strength * n)):
        i, j = sorted(random.sample(range(n), 2))
        path[i:j] = reversed(path[i:j])
    return path