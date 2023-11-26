import re

from .evaluate import *
from .property import *


def get_match_compare(condition, context):
    expression = condition.children[0]
    expression = get_expression(expression, context)
    value = condition.children[1]
    value = get_value(value, context)
    if type(expression) is not str or type(value) is not str:
        raise Exception("Match compare only support string")
    if len(condition.children) == 2:
        return re.match(value, expression)
    else:
        variable = condition.children[2]
        variable = get_variable_name(variable)
        result = re.search(value, expression)
        if result:
            context.set_variable(variable, result.group())
        return True


def get_larger_compare(condition, context):
    first_expression = condition.children[0]
    second_expression = condition.children[1]
    first_value = get_expression(first_expression, context)
    second_value = get_expression(second_expression, context)
    return first_value > second_value


def get_less_compare(condition, context):
    first_expression = condition.children[0]
    second_expression = condition.children[1]
    first_value = get_expression(first_expression, context)
    second_value = get_expression(second_expression, context)
    return first_value < second_value


def get_condition(condition, context):
    condition = condition.children[0]
    condition_type = condition.data
    match condition_type:
        case "match_compare":
            return get_match_compare(condition, context)
        case "equal_compare":
            return get_equal_compare(condition, context)
        case "larger_compare":
            return get_larger_compare(condition, context)
        case "less_compare":
            return get_less_compare(condition, context)
        case "timeout":
            return context.timeout
        case "boolean":
            return get_boolean(condition)


def get_equal_compare(condition, context):
    first_expression = condition.children[0]
    second_expression = condition.children[1]
    first_value = get_expression(first_expression, context)
    second_value = get_expression(second_expression, context)
    return first_value == second_value
