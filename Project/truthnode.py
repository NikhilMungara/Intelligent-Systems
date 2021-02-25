from __future__ import print_function, unicode_literals
import argparse
from forseti.formula import Formula, Predicate, Symbol, Not, And, Or, If, Iff
import forseti.parser
from six import string_types

# TruthNode: represents a node in the tree
'''
    list_of_formulas: contains all the formulas
    node_parent: pointer to node parent
    list_of_child: contains all child
    is_closed: to represent whether the node is closed
    index: index of the node
'''
class TruthNode(object):
    def __init__(self):
        self.list_of_formulas = []
        self.node_parent = None
        self.list_of_child = []
        self.is_closed = False
        self.index = None

    # adds a new formula to the list_of_formula 
    def add_formula(self, input_formula, index):
        if self.is_closed:
            return False
        self.list_of_formulas.append(input_formula)
        temp = Not(input_formula.formula) if not isinstance(input_formula.formula, Not) else input_formula.formula.args[0]
        if self.check_if_formula_present(temp):
            self.is_closed = True
            self.index = index
            return True
        return False

    #check if a formula already exists
    def check_if_formula_present(self, input_formula):
        for f in self.list_of_formulas:
            if f.formula == input_formula:
                return True
        if self.node_parent is None:
            return False
        return self.node_parent.check_if_formula_present(input_formula)

    # check if the node is closed
    def check_if_closed(self):
        if len(self.list_of_child) == 0:
            return self.is_closed
        list_of_closed_children = []
        for c in self.list_of_child:
            list_of_closed_children.append(c.check_if_closed())
        return not (False in list_of_closed_children)

    # check whether the node can be expanded
    def check_expansion(self):
        if self.is_closed:
            return False
        for f in self.list_of_formulas:
            if f.is_broken is False:
                return True
        temp = []
        for c in self.list_of_child:
            temp.append(c.check_expansion())
        return True in temp

    # add new child and return the new list of left and right children
    def add_child(self):
        if self.is_closed:
            return [[], []]
        elif len(self.list_of_child) == 0:
            for i in range(2):
                n = TruthNode()
                n.node_parent = self
                self.list_of_child.append(n)
            return [self.list_of_child[0]], [self.list_of_child[1]]
        else:
            list_of_left_nodes = []
            list_of_right_nodes = []
            for c in self.list_of_child:
                left, right = c.add_child()
                list_of_left_nodes.extend(left)
                list_of_right_nodes.extend(right)
            return list_of_left_nodes, list_of_right_nodes

    # retrive all children
    def get_all_children(self):
        if self.is_closed:
            return []
        elif len(self.list_of_child) == 0:
            return [self]
        else:
            temp = []
            for c in self.list_of_child:
                temp.extend(c.get_all_children())
            return temp

