# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import argparse
from forseti.formula import Formula, Predicate, Symbol, Not, And, Or, If, Iff
import forseti.parser
from six import string_types
from truthnode import TruthNode
from formulatree import FormulaTree
from truthtree import TruthTree

def generate_format(formula):
    
    if isinstance(formula, Symbol) or isinstance(formula, Predicate):
        text = str(formula)
    elif isinstance(formula, Not):
        text = "¬" + generate_format(formula.args[0])
    else:
        temp = []
        for arg in formula.args:
            temp.append(generate_format(arg))
        if isinstance(formula, And):
            text = " ∧ ".join(temp)
        elif isinstance(formula, Or):
            text = " ∨ ".join(temp)
        elif isinstance(formula, If):
            text = " → ".join(temp)
        elif isinstance(formula, Iff):
            text = " ↔ ".join(temp)
        else:
            raise TypeError("Invalid Formula Type: " + str(type(formula)))
        text = "(" + text + ")"
    return text.strip()


def exec(input_formula, input_goal):
    #convert the formula to list
    if isinstance(input_formula, string_types):
        input_formula = [input_formula]

    #check if valid goal, else raise error
    if not isinstance(input_goal, string_types):
        raise TypeError("Invalid input provided for goal" + str(type(input_goal)))

    list_of_formula = []
    for f in input_formula:
        f = f.strip()
        if len(f) > 0:
            list_of_formula.append(forseti.parser.parse(f))

    #parse the goal
    parsed_goal = forseti.parser.parse(input_goal)
    return TruthTree(list_of_formula, parsed_goal)

