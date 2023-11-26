from .setters import *
from .. import get_tributary


def run_handover(statement, context, speak_function, listen_function):
    tributary_name = get_tributary_name(statement.children[0])
    tributary = get_tributary(tributary_name)
    if tributary is None:
        raise Exception(f"Tributary {tributary_name} not found")
    tributary(context, speak_function, listen_function)


def run_assign(statement, context):
    expression = statement.children[0]
    value = get_expression(expression, context)
    variable = statement.children[1]
    variable_name = get_variable_name(variable)
    context.set_variable(variable_name, value)


def run_speak(statement, context, speak_function):
    value = get_expression(statement.children[0], context)
    speak_function(value)


def run_listen(statement, context, listen_function):
    length = len(statement.children)
    match length:
        case 1:
            value = listen_function()
            set_variable(statement.children[0], context, value)
        case 2:
            timer = get_time(statement.children[1], context)
            value = listen_function(timer)
            if value is None:
                context.set_timeout(True)
            else:
                set_variable(statement.children[0], context, value)
