from .getters import *
from .. import get_tributary


def run_handover(statement, context):
    tributary_name = get_tributary_name(statement.children[0])
    tributary = get_tributary(tributary_name)
    if tributary is None:
        raise Exception(f"Tributary {tributary_name} not found")
    tributary(context)


def run_assign(statement, context):
    expression = statement.children[0]
    value = get_expression(expression, context)
    variable = statement.children[1]
    variable_name = get_variable_name(variable)
    context.set_variable(variable_name, value)
