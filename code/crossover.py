# 交叉遗传函数
import random

def pmx_crossover(parent1, parent2):
    """
    映射交叉
    """
    n = len(parent1)
    child1 = [None] * n
    child2 = [None] * n
    start, end = sorted([random.randint(0, n-1) for i in range(2)])
    child1[start:end+1] = parent1[start:end+1]
    child2[start:end+1] = parent2[start:end+1]

    
    def pmx_fill(child, parent_other):
        for i in range(start, end+1):
            tmp = parent_other[i]
            if tmp not in child:
                pos = i
                while True:
                    gen_in_child = child[pos]
                    pos = parent_other.index(gen_in_child)
                    if child[pos] is None:
                        child[pos] = tmp
                        break
        for i in range(n):
            if child[i] is None:
                child[i] = parent_other[i]
        return child
    
    child1 = pmx_fill(child1, parent2)
    child2 = pmx_fill(child2, parent1)
    return child1, child2


def order_crossover(parent1, parent2):
    """
    顺序交叉
    """
    n = len(parent1)
    child1 = [0] * n
    child2 = [0] * n
    start, end = sorted([random.randint(0, n - 1) for _ in range(2)])
    child1[start:end+1] = parent1[start:end+1]
    child2[start:end+1] = parent2[start:end+1]

    pos1 = (end + 1) % n
    for i in parent1:
        if i not in child2:
            child2[pos1] = i
            pos1 = (pos1 + 1) % n
    pos2 = (end + 1) % n
    for i in parent2:
        if i not in child1:
            child1[pos2] = i
            pos2 = (pos2 + 1) % n
    return child1, child2