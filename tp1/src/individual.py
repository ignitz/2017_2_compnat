from random import random, randint, uniform

from tree import *

import copy

class Individual:

    def __init__(self, size_vars, min_depth=1, max_depth=3):
        self.size_vars = size_vars
        self.fitness = None
        self.tree = Node(generate_tree(size_vars, min_depth, max_depth))
        self.min_depth = min_depth
        self.max_depth = max_depth

    def set_fitness(self, x_values, fx_values):
        abs_error = 0.0
        if type(x_values) is not list:
            raise Exception('x_values is not list, it\'s ' + str(type(x_values)))

        for x, y in zip(x_values, fx_values):
            result = self.tree.evaluation(x)
            abs_error += abs(result - y)

        self.fitness = abs_error
        return abs_error

    def _walk_subtree(self, _tree, parent, depth, height, left_or_right=None):
        if height > depth:
            raise Exception('height is greater then desire depth walking on tree')

        # make mutation
        if depth == height:
            return _tree, parent, left_or_right

        if type(_tree) is Operator:
            if randint(0,1) == 0: #left or right
                return self._walk_subtree(_tree.node_left, _tree, depth, height + 1, 'left')
            else:
                return self._walk_subtree(_tree.node_right, _tree, depth, height + 1, 'right')
        elif type(_tree) is Constant:
            return _tree, parent, None
        elif type(_tree) is Sin or \
                type(_tree) is Cos or \
                type(_tree) is Log or \
                type(_tree) is Exp:
            return self._walk_subtree(_tree.children, _tree, depth, height + 1)

    def do_mutation(self, mut_prob):
        if random() < mut_prob:
            depth = randint(1, self.max_depth)
            node_to_mutate, parent, left_or_right = self._walk_subtree(self.tree.children, self.tree, depth, 1)

            what_type = randint(1, 3)
            if what_type == 1:
                new_node = Constant(uniform(-5.0, 5.0))
            elif what_type == 2:
                new_node = Variable(randint(1, self.size_vars))
            elif what_type == 3:
                new_node = generate_tree(self.size_vars, self.min_depth, self.max_depth)

            if type(parent) is Node:
                parent.children = new_node
            elif type(parent) is Operator:
                if left_or_right == 'left':
                    parent.node_left = new_node
                else:
                    parent.node_right = new_node
            else:
                parent.children = new_node

    def do_crossover(self, other, cross_prob):
        if random() < cross_prob:

            aux_1 = copy.deepcopy(self)
            aux_2 = copy.deepcopy(other)

            depth = randint(1, aux_1.max_depth)
            node_a, parent_a, left_or_right_a = aux_1._walk_subtree(aux_1.tree.children, aux_1.tree, depth, 1)
            depth = randint(1, aux_2.max_depth)
            node_other, parent_other, left_or_right_other = aux_2._walk_subtree(aux_2.tree.children, aux_2.tree, depth, 1)

            if type(parent_a) is Node:
                parent_a.children = copy.deepcopy(node_other)
            elif type(parent_a) is Operator:
                if left_or_right_a == 'left':
                    parent_a.node_left = copy.deepcopy(node_other)
                else:
                    parent_a.node_right = copy.deepcopy(node_other)
            else:
                parent_a.children = copy.deepcopy(node_other)

            if type(parent_other) is Node:
                parent_other.children = copy.deepcopy(node_a)
            elif type(parent_other) is Operator:
                if left_or_right_other == 'left':
                    parent_other.node_left = copy.deepcopy(node_a)
                else:
                    parent_other.node_right = copy.deepcopy(node_a)
            else:
                parent_other.children = copy.deepcopy(node_a)

            return aux_1, aux_2
        else:
            return None, None

    def __str__(self):
        return str(self.tree)

def test_mutation():
    ind = Individual(1)
    print(ind)

    x_values = [[0.0], [0.5], [1.0]]
    fx_values = [0.0, -0.6931471805599, 0.0]

    ind.do_mutation(1.0)
    print(ind)

def test_crossover():
    while True:
        ind1 = Individual(1)
        ind2 = Individual(1)
        print_bold(ind1)
        print_error(ind2)

        children1, children2 = ind1.do_crossover(ind2, 1.0)

        print_green(children1)
        print_purple(children2)
        print("-------------------------------------------------")


if __name__ == '__main__':
    # while True:
    #     ind = Individual(1)
    #     print(ind)
    #
    #     x_values = [[0.0], [0.5], [1.0]]
    #     fx_values = [0.0, -0.6931471805599, 0.0]
    #
    #     ind.set_fitness(x_values, fx_values)
    #
    #     print(ind.fitness)

    test_mutation()
    test_crossover()