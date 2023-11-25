import re

from . import get_tributary
from .context import Context


def get_literal(tree):
    value = tree.children[0]
    match value.type:
        case "STRING_LITERAL":
            value = value.value[1:-1]
            # value = replace_question_string(value, context)
        case "NUMBER_LITERAL":
            value = int(value.value)
    return value


def get_variable(value, context):
    variable_name = value.children[0].value
    return context.get_variable(variable_name)


def get_value(tree, context):
    value = tree.children[0]
    match value.data:
        case "literal":
            return get_literal(value)
        case "variable":
            variable_name = get_variable_name(value)
            return context.get_variable(variable_name)


def get_identifier(tree):
    return tree.children[0].value


def set_variable(tree, context, value):
    variable_name = get_variable_name(tree)
    context.set_variable(variable_name, value)


def get_variable_name(tree):
    return get_identifier(tree.children[0])


def get_time(tree, context):
    timer = tree.children[0]
    timer = get_value(timer, context)
    unit = tree.children[1].children[0].data
    match unit:
        case "second":
            timer *= 1
        case "minute":
            timer *= 60
        case "hour":
            timer *= 3600
    return timer


def get_flow_name(tree):
    name = get_identifier(tree.children[0])
    return name


def get_tributary_name(tree):
    name = get_identifier(tree.children[0])
    return name


def run_handover(statement, context):
    tributary_name = get_tributary_name(statement.children[0])
    tributary = get_tributary(tributary_name)
    if tributary is None:
        raise Exception(f"Tributary {tributary_name} not found")
    tributary(context)


def get_boolean(condition):
    condition = condition.children[0]
    if condition.type == "TRUE":
        return True
    elif condition.type == "FALSE":
        return False
    else:
        raise Exception("Unknown boolean")


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


def get_equal_compare(condition, context):
    first_expression = condition.children[0]
    second_expression = condition.children[1]
    first_value = get_expression(first_expression, context)
    second_value = get_expression(second_expression, context)
    return first_value == second_value


def run_assign(statement, context):
    expression = statement.children[0]
    value = get_expression(expression, context)
    variable = statement.children[1]
    variable_name = get_variable_name(variable)
    context.set_variable(variable_name, value)


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


class Runtime:
    def __init__(self, tree, speak_function, listen_function):
        self.tree = tree
        self.speak_function = speak_function
        self.listen_function = listen_function
        self.flow_dict = {}
        self.symbol_table = {}
        self.exit = False
        self.register_flow()
        self.contextStack = []

    def register_flow(self):
        for flow in self.tree.children:
            flow_name = flow.children[0].children[0].children[0]
            block = flow.children[1]
            self.flow_dict[flow_name] = block

    def run(self):
        self.run_flow("origin")

    def run_flow(self, flow_name, parameter=None):
        if flow_name not in self.flow_dict:
            raise Exception(f"Flow {flow_name} not found")
        tree = self.flow_dict[flow_name]
        context = Context(parameter, tree)
        self.contextStack.append(context)
        self.run_block(tree, context)
        self.contextStack.pop()

    def run_block(self, block, context):
        context.push_scope()
        for statement in block.children:
            if self.exit:
                return
            self.run_statement(statement, context)

    def run_statement(self, statement, context):
        statement = statement.children[0]
        state_type = statement.data
        match state_type:
            case "speak_statement":
                self.run_speak(statement, context)
            case "listen_statement":
                self.run_listen(statement, context)
            case "if_statement":
                self.run_if(statement, context)
            case "engage_statement":
                self.run_engage(statement, context)
            case "assign_statement":
                run_assign(statement, context)
            case "end_statement":
                self.exit = True
            case "handover_statement":
                run_handover(statement, context)
            case "while_statement":
                self.run_while(statement, context)

    def run_speak(self, statement, context):
        value = get_expression(statement.children[0], context)
        self.speak_function(value)

    def run_listen(self, statement, context):
        length = len(statement.children)
        match length:
            case 1:
                value = self.listen_function()
                set_variable(statement.children[0], context, value)
            case 2:
                timer = get_time(statement.children[1], context)
                value = self.listen_function(timer)
                if value is None:
                    context.set_timeout(True)
                else:
                    set_variable(statement.children[0], context, value)

    def run_if(self, statement, context):
        condition = statement.children[0]
        result = get_condition(condition, context)
        if result:
            self.run_block(statement.children[1], context)
        else:
            if len(statement.children) == 3:
                self.run_else(statement.children[2], context)

    def run_else(self, statement, context):
        else_statement = statement.children[0]
        match else_statement.data:
            case "block":
                self.run_block(else_statement, context)
            case "if_statement":
                self.run_if(else_statement, context)

    def run_engage(self, statement, context):
        flow_name = get_flow_name(statement.children[0])
        self.run_flow(flow_name, context.get_parameter())

    def run_while(self, statement, context):
        condition = statement.children[0]
        while get_condition(condition, context):
            self.run_block(statement.children[1], context)
