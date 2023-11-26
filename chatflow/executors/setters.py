from .getters import *


def set_variable(tree, context, value):
    variable_name = get_variable_name(tree)
    context.set_variable(variable_name, value)
