from __future__ import print_function, unicode_literals
import argparse
from forseti.formula import Formula, Predicate, Symbol, Not, And, Or, If, Iff
import forseti.parser
from six import string_types
from truthnode import TruthNode
from formulatree import FormulaTree

class TruthTree(object):
    def __init__(self, input_formulas, input_goal):
        self.root_node = TruthNode()
        for formula in input_formulas:
            self.root_node.list_of_formulas.append(FormulaTree(formula))
        self.root_node.list_of_formulas.append(FormulaTree(Not(input_goal)))
        self.index = 1
        self.expand_tree()

    def check_if_already_expanded(self):
        return self.root_node.check_if_closed() or not self.root_node.check_expansion()

    def expand_tree(self):
        while not self.check_if_already_expanded():
            self.perform_expansion(self.root_node)

    def perform_expansion(self, tree_node):
        if tree_node.check_if_closed():
            return False

        for formula in tree_node.list_of_formulas:
            assert(isinstance(formula, FormulaTree))
            if not formula.is_broken and formula.can_be_broken():
                self.expand_formula(formula, tree_node)
                return True

        for c in tree_node.list_of_child:
            if self.perform_expansion(c):
                return True
        return False

    def add_formula(self, tree_node, formula):
        if tree_node.add_formula(FormulaTree(formula), self.index):
            self.index += 1
            return True
        return False

    def expand_formula(self, tree_formula, tree_node):
        tree_formula.index = self.index
        tree_formula.is_broken = True
        self.index += 1
        formula = tree_formula.formula

        
        if isinstance(formula, Not):
            if isinstance(formula.args[0], Not):
                list_of_child = tree_node.get_all_children()
                for child in list_of_child:
                    self.add_formula(child, formula.args[0].args[0])
            elif isinstance(formula.args[0], And):
                left_nodes, right_nodes = tree_node.add_child()
                for node in left_nodes:
                    self.add_formula(node, Not(formula.args[0].args[0]))
                for node in right_nodes:
                    self.add_formula(node, Not(formula.args[0].args[1]))
            elif isinstance(formula.args[0], Or):
                list_of_child = tree_node.get_all_children()
                for child in list_of_child:
                    for i in range(2):
                        if self.add_formula(child, Not(formula.args[0].args[i])):
                            break
            elif isinstance(formula.args[0], If):
                list_of_child = tree_node.get_all_children()
                for child in list_of_child:
                    if self.add_formula(child, formula.args[0].args[0]):
                        continue
                    self.add_formula(child, Not(formula.args[0].args[1]))
            elif isinstance(formula.args[0], Iff):
                left_nodes, right_nodes = tree_node.add_child()
                for node in left_nodes:
                    if self.add_formula(node, formula.args[0].args[0]):
                        continue
                    self.add_formula(node, Not(formula.args[0].args[1]))
                for node in right_nodes:
                    if self.add_formula(node, Not(formula.args[0].args[0])):
                        continue
                    self.add_formula(node, formula.args[0].args[1])
        elif isinstance(formula, And):
            list_of_child = tree_node.get_all_children()
            for node in list_of_child:
                for i in range(2):
                    if self.add_formula(node, formula.args[i]):
                        break
        elif isinstance(formula, Or):
            left_nodes, right_nodes = tree_node.add_child()
            for node in left_nodes:
                self.add_formula(node, formula.args[0])
            for node in right_nodes:
                self.add_formula(node, formula.args[1])
        elif isinstance(formula, If):
            left_nodes, right_nodes = tree_node.add_child()
            for node in left_nodes:
                self.add_formula(node, Not(formula.args[0]))
            for node in right_nodes:
                self.add_formula(node, formula.args[1])
        elif isinstance(formula, Iff):
            left_nodes, right_nodes = tree_node.add_child()
            for node in left_nodes:
                for i in range(2):
                    if self.add_formula(node, formula.args[i]):
                        break
            for node in right_nodes:
                for i in range(2):
                    if self.add_formula(node, Not(formula.args[i])):
                        break
