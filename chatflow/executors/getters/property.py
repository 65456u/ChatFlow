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


def get_boolean(condition):
    condition = condition.children[0]
    if condition.type == "TRUE":
        return True
    elif condition.type == "FALSE":
        return False
    else:
        raise Exception("Unknown boolean")
