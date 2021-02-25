from __future__ import print_function, unicode_literals
import argparse
from forseti.formula import Formula, Predicate, Symbol, Not, And, Or, If, Iff
import forseti.parser
from six import string_types

class FormulaTree(object):
    def __init__(self, input_formula):
        self.formula = input_formula
        self.is_broken = not self.can_be_broken()
        self.index = None

    def can_be_broken(self):
        return not ((isinstance(self.formula.args[0], Symbol) and isinstance(self.formula, Not)) or isinstance(self.formula, Symbol))

    def print_representation(self):
        return repr(self.formula)


