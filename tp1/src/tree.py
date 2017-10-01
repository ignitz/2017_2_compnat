from utils import *
from random import randint, uniform
import math

# class Type:
#     Operator = 1
#     Constant = 2
#     Variable = 3
#     Function = 4

class Operator_Type:
    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4

class Node(object):

    def __init__(self, first_node):
        self.children = first_node

    def evaluation(self):
        pass

    def __str__(self):
        return str(self.children)

class Operator(Node):

    def __init__(self, operator, node_left=None, node_right=None):
        super().__init__(None)
        if type(node_left) is Constant and type(node_right ) is Constant:
            print('Sum two constants')
        self.node_left = node_left
        self.node_right = node_right
        self.operator = operator

    def evaluation(self, values):
        return {
            Operator_Type.ADD: (self.node_left.evaluation(values) + self.node_right.evaluation(values)),
            Operator_Type.SUB: (self.node_left.evaluation(values) - self.node_right.evaluation(values)),
            Operator_Type.MUL: (self.node_left.evaluation(values) * self.node_right.evaluation(values)),
            Operator_Type.DIV: (self.node_left.evaluation(values) / self.node_right.evaluation(values) \
                           if self.node_right.evaluation(values) != 0 else 1.0 )
        }[self.operator]

    def __str__(self):
        return {
            Operator_Type.ADD: ('(' + str(self.node_left) + ' + ' + str(self.node_right)) + ')',
            Operator_Type.SUB: ('(' + str(self.node_left) + ' - ' + str(self.node_right)) + ')',
            Operator_Type.MUL: ('(' + str(self.node_left) + ' * ' + str(self.node_right)) + ')',
            Operator_Type.DIV: ('(' + str(self.node_left) + ' / ' + str(self.node_right)) + ')'
        }[self.operator]

class Variable(Node):

    def __init__(self, index=1, node_value=None):
        super().__init__(None)
        self.index = index

    def evaluation(self, values):
        return float(values[self.index - 1])

    def __str__(self):
        res = 'X' + str(self.index)
        return res

class Constant(Node):

    def __init__(self, value):
        super().__init__(None)
        self.value = float(value)

    def evaluation(self, values):
        return self.value

    def __str__(self):
        return str(self.value)

"""-------------------------------------------------------"""

class Function(Node):

    def __init__(self, node=None):
        super().__init__(None)
        self.children = node

    def evaluation(self, values):
        return 0.0

class Sin(Function):

    def __init__(self, children_node):
        super().__init__(children_node)

    def evaluation(self, values):
        return math.sin(self.children.evaluation(values))

    def __str__(self):
        return 'sin(' + str(self.children) + ')'

class Cos(Function):

    def __init__(self, children_node):
        super().__init__(children_node)

    def evaluation(self, values):
        return math.cos(self.children.evaluation(values))

    def __str__(self):
        return 'cos(' + str(self.children) + ')'

class Log(Function):

    def __init__(self, children_node):
        super().__init__(children_node)

    def evaluation(self, values):
        value = self.children.evaluation(values)
        if value > 0.0:
            return math.log(self.children.evaluation(values))
        else:
            return 0.0

    def __str__(self):
        return 'ln(' + str(self.children) + ')'

class Exp(Function):

    def __init__(self, children_node):
        super().__init__(children_node)

    def evaluation(self, values):
        return math.exp(self.children.evaluation(values))

    def __str__(self):
        return 'exp(' + str(self.children) + ')'

"""------------------------------------------------"""
"""Generate tree"""

def generate_tree(size_vars, min_depth=1, max_depth=2, depth=0):
    if depth == max_depth:
        return Constant(uniform(-5, 5)) if randint(0, 1) == 0 else Variable(randint(1, size_vars))
    else:
        which_operator = randint(1, 8)
        # +
        if 1 <= which_operator <= 4:
            node_left = generate_tree(size_vars, min_depth, max_depth, depth + 1)
            node_right = generate_tree(size_vars, min_depth, max_depth, depth + 1)
            if type(node_left) is Constant and type(node_right) is Constant:
                # +
                if which_operator == 1:
                    return Constant(node_left.evaluation([]) + node_right.evaluation([]))
                # -
                elif which_operator == 2:
                    return Constant(node_left.evaluation([]) - node_right.evaluation([]))
                # *
                elif which_operator == 3:
                    return Constant(node_left.evaluation([]) * node_right.evaluation([]))
                # /
                elif which_operator == 4:
                    if node_right.evaluation([]) != 0:
                        return Constant(node_left.evaluation([]) / node_right.evaluation([]))
                    else:
                        return Constant(node_left.evaluation([]) / 1.0)
            else:
                # +
                if which_operator == 1:
                    return Operator(Operator_Type.ADD, node_left, node_right)
                # -
                elif which_operator == 2:
                    return Operator(Operator_Type.SUB, node_left, node_right)
                # *
                elif which_operator == 3:
                    return Operator(Operator_Type.MUL, node_left, node_right)
                # /
                elif which_operator == 4:
                    if type(node_right) is Constant:
                        if node_right.evaluation([]) == 0:
                            return node_left
                    return Operator(Operator_Type.DIV, node_left, node_right)

        elif which_operator >= 5:
            node_children = generate_tree(size_vars, min_depth, max_depth, depth)
            # sin
            if which_operator == 5:
                return Sin(node_children)
            # cos
            elif which_operator == 6:
                return Cos(node_children)
            # log
            elif which_operator == 7:
                return Log(node_children)
            # exp
            elif which_operator == 8:
                return Exp(node_children)
            else:
                raise Error('Unknow operator inserted')


if __name__ == '__main__':
    a_tree = generate_tree(10, 1, 5)

    print(a_tree)
    # node_left = Constant(0.5)
    # node_right = Constant(0.5)
    # values = [5.0]
    # node = Operator(Operator_Type.ADD, node_left, node_right)
    # print(node.evaluation(values))
    #
    # print(Exp(node))
    # print(Exp(node).evaluation(values))
    #
    # values = [1.0, 2.0, 3.0]
    # node = Operator(Operator_Type.ADD, Variable(1), Operator(Operator_Type.ADD, Variable(2), Variable(3)))
    # print(node)
    #
    # print(node.evaluation(values))
    #
    # values = [math.pi]
    #
    # node = Cos(Variable(1))
    # print(node.evaluation(values))

