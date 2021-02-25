# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask import Flask, Markup, render_template, request, jsonify
import main

CLOSED_STRING = "<span style='color: red;'>X</span>"
FLASK_APP = Flask(__name__,template_folder='view')


@FLASK_APP.route("/")
def index_page():
    return render_template('home.html')


@FLASK_APP.route("/submit", methods=['POST'])
def generate_tree():

    
    goal=request.json['goal']
    formulas = request.json['formulas']
    try:
        tree = main.exec(formulas, goal)
    except (SyntaxError, TypeError) as exception:
        return render_template('validation.html', error=str(exception))
    
    tree_render = render_node(tree.root_node)
    return render_template('truthtree.html', tree=tree_render, closed=tree.root_node.check_if_closed())


def render_node(node):
    children = []
    for child in node.list_of_child:
        children.append(render_node(child))

    formulas = []
    for formula in node.list_of_formulas:
        formulas.append(main.generate_format(formula.formula))
    if node.is_closed:
        formulas.append(Markup(CLOSED_STRING))
    return Markup(render_template('truthnode.html', formulas=formulas, children=children))


if __name__ == '__main__':
    FLASK_APP.debug = True
    FLASK_APP.run()