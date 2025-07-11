# 辅助函数文件

import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import numpy as np


def distance_cites(cities):
    cities = np.array(cities)
    n = len(cities)
    diff = cities[:, np.newaxis, :] - cities[np.newaxis, :, :]
    dist_matrix = np.sqrt(np.sum(diff ** 2, axis=2))
    return dist_matrix

def get_total(dist_matrix, path):
    path = np.array(path)
    next_path = np.roll(path, -1)
    return np.sum(dist_matrix[path, next_path])

def fitness(dist_matrix, path):
    return 1.0 / get_total(dist_matrix, path)


def population_diversity(population):
    """
    多样性测试
    """
    total_diff = 0
    n = len(population[0])
    base = population[0]
    for ind in population[1:]:
        diff = sum(1 for i, j in zip(base, ind) if i != j)
        total_diff += diff
    return total_diff / ((len(population) - 1) * n)


def load_tsp_file(filepath):
    cities = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
        start = False
        for line in lines:
            if line.strip() == "NODE_COORD_SECTION":
                start = True
                continue
            if line.strip() == "EOF":
                break
            if start:
                parts = line.strip().split()
                if len(parts) >= 3:
                    x = float(parts[1])
                    y = float(parts[2])
                    cities.append((x, y))
    return cities

def plot_tsp_path(cities, path, title="Best Path", save_path=None):
    x = [cities[i][0] for i in path + [path[0]]]
    y = [cities[i][1] for i in path + [path[0]]]
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o', linestyle='-', linewidth=1.5)
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
    plt.close()

def plot_convergence(best_list, avg_list, save_path=None):
    plt.figure(figsize=(8, 5))
    plt.plot(best_list, label="Best Path Length")
    plt.plot(avg_list, label="Average Path Length")
    plt.title("GA Convergence")
    plt.xlabel("Generation")
    plt.ylabel("Distance")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
    plt.close()
