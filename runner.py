def run_flow(flow_name):
    if flow_name not in flow_dict:
        raise Exception("Flow not found")
    print("running flow:", flow_name)
    block = flow_dict[flow_name]
    run_block(block)


def run_block(block):
    for statement in block.children:
        run_statement(statement)


def run_statement(statement):
    stmt=statement.children[0]
    match stmt.data:
        case "if_statement":
            run_if_statement(stmt)
        case "speak_statement":
            run_speak_statement(stmt)
        case "goto_statement":
            run_goto_statement(stmt)
        case "handover_statement":
            run_handover_statement(stmt)
        case "end_statement":
            run_end_statement(stmt)
        case "listen_statement":
            run_listen_statement(stmt)
        case "assign_statement":
            run_assign_statement(stmt)


def run_if_statement(statement):
    condition = statement.children[0]
    if_condition = evaluate_condition(condition)
    if if_condition:
        run_block(statement.children[1])
    else:
        run_block(statement.children[2])


def run_speak_statement(statement):
    value=get_value(statement.children[0])
    print(value)

def get_value(tree):
    value=tree.children[0]
    match value.data:
        case "literal":
            return get_literal(value)
        case "identifier":
            return get_identifier_value(value)

def get_identifier_value(tree):
    return ""

def get_literal(tree):
    return tree.children[0].value
def evaluate_condition(condition_tree):
    # Add your logic to evaluate the condition here
    return True  # For simplicity, always return True


def run_goto_statement(statement):
    flow_name = statement.children[0]
    run_flow(flow_name)


def run_handover_statement(statement):
    script_name = statement.children[0]
    print("Handover to script:", script_name)


def run_end_statement(statement):
    print("End of flow")


def run_listen_statement(statement):
    variable = statement.children[0]
    print("Listening for variable:", variable)


def run_assign_statement(statement):
    identifier = statement.children[0]
    expression = statement.children[1]
    variable_dict[identifier] = expression
    print("Assigning variable:", identifier, "=", expression)
