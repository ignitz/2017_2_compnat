from random import random, randint

from tree import *

class Individual:

    def __init__(self, size_vars):
        self.fitness = None
        self.tree = generate_tree(size_vars, 1, 2)

    def set_fitness(self, values_list):
        pass

    def mutation(self, prob):
        if random() < prob:
            depth = randint(1, self.max_depth)
            affected_node = self.tree

    def __str__(self):
        return str(self.tree)


if __name__ == '__main__':
    ind = Individual(2)
    print(ind)