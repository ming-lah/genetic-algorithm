# 初始化种群文件

import random
import numpy as np



def nearest_neighbor(dist_matrix):
    """
    加入邻近最优
    """
    n = len(dist_matrix)
    unvisited = set(range(n))
    current = random.choice(list(unvisited))
    path = [current]
    unvisited.remove(current)
    while unvisited:
        next = min(unvisited, key=lambda city: dist_matrix[current][city])
        path.append(next)
        unvisited.remove(next)
        current = next
    return path


def farthest_insertion(dist_matrix):
    """
    邻近最远启发式
    """
    n = len(dist_matrix)
    remaining = list(range(n))
    tour = [random.choice(remaining)]
    remaining.remove(tour[0])

    farthest = max(remaining, key=lambda x: dist_matrix[tour[0]][x])
    tour.append(farthest)
    remaining.remove(farthest)

    while remaining:
        next_city = max(remaining, key=lambda x: min(dist_matrix[x][c] for c in tour))

        best_pos, best_cost = 0, float('inf')
        for i in range(len(tour)):
            a, b = tour[i], tour[(i+1) % len(tour)]
            cost = dist_matrix[a][next_city] + dist_matrix[next_city][b] - dist_matrix[a][b]
            if cost < best_cost:
                best_pos, best_cost = i+1, cost

        tour.insert(best_pos, next_city)
        remaining.remove(next_city)
    return tour


def random_shuffle(num_cities):
    """
    随机解
    """
    path = list(range(num_cities))
    random.shuffle(path)
    return path

def init_populations(pop_size, num_size, dist_matrix, strategy):
    """
    初始化种群
    """
    populations = []
    base = np.arange(num_size)
    if strategy == 'nearest':
        populations.append(nearest_neighbor(dist_matrix))
        rand_part = [np.random.permutation(base).tolist() for i in range(pop_size - 1)]
        populations.extend(rand_part)
        return populations
    elif strategy == 'random':
        populations = [np.random.permutation(base).tolist() for _ in range(pop_size)]
        return populations
    elif strategy == 'farthest':
        populations.append(farthest_insertion(dist_matrix))
        rand_part = [np.random.permutation(base).tolist() for i in range(pop_size - 1)]
        populations.extend(rand_part)
        return populations
    else:
        populations.append(farthest_insertion(dist_matrix))
        populations.append(nearest_neighbor(dist_matrix))
        rand_part = [np.random.permutation(base).tolist() for i in range(pop_size - 2)]
        populations.extend(rand_part)
        return populations

