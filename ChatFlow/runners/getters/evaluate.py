from .property import *


def get_factor(factor, context):
    factor = factor.children[0]
    if factor.data == "value":
        result = get_value(factor, context)
    else:
        result = get_expression(factor, context)
    return result


def get_term(term, context):
    factor = term.children[0]
    value = get_factor(factor, context)
    for i in range(1, len(term.children), 2):
        operator = term.children[i].children[0]
        factor = term.children[i + 1]
        factor_value = get_factor(factor, context)
        if operator.type == "TIMES":
            value *= factor_value
        elif operator.type == "DIVIDE":
            value /= factor_value
    return value


def get_expression(expression, context):
    term = expression.children[0]
    value = get_term(term, context)
    for i in range(1, len(expression.children), 2):
        operator = expression.children[i].children[0]
        term = expression.children[i + 1]
        term_value = get_term(term, context)
        if operator.type == "PLUS":
            value += term_value
        elif operator.type == "MINUS":
            value -= term_value
    return value
