import random
from utils import fitness

def selection(populations, dist_matrix):
    """
    轮盘赌
    """
    fits = [fitness(dist_matrix, path) for path in populations]
    total = sum(fits)
    new_populatiions = []
    for i in range(len(populations)):
        pick = random.random() * total
        current = 0
        for path, f in zip(populations, fits):
            current += f
            if current > pick:
                new_populatiions.append(path[:])
                break
    return new_populatiions

def tournament_selcetion(populations, dist_matrix, size=3):
    """
    锦标赛
    """
    new_population = []
    n = len(populations)
    for i in range(n):
        tournament = random.sample(populations, size)
        winner = max(tournament, key=lambda ind: fitness(dist_matrix, ind))
        new_population.append(winner[:])
    return new_population