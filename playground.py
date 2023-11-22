from lark import Lark

dsl_grammar = """
start: statement+

statement: if_statement | while_statement | expression

if_statement: "if" condition "{" statement+ "}" "else" "{" statement+ "}"

while_statement: "while" condition "{" statement+ "}"

condition: expression

expression: /[a-zA-Z]+/

%ignore /\s+/
"""

dsl_parser = Lark(dsl_grammar)


def handle_statement(tree):
    for statement in tree.children:
        if statement.data == "if_statement":
            handle_if_statement(statement)
        elif statement.data == "while_statement":
            handle_while_statement(statement)
        elif statement.data == "expression":
            handle_expression(statement)


def handle_if_statement(tree):
    condition = tree.children[0]
    if_condition = evaluate_condition(condition)
    if if_condition:
        handle_statement(tree.children[1])
    else:
        handle_statement(tree.children[2])


def handle_while_statement(tree):
    condition = tree.children[0]
    while_condition = evaluate_condition(condition)
    while while_condition:
        handle_statement(tree.children[1])
        while_condition = evaluate_condition(condition)


def handle_expression(tree):
    variable = tree.children[0].value
    print("Processing expression:", variable)


def evaluate_condition(condition_tree):
    variable = condition_tree.children[0].value
    # Add your logic to evaluate the condition here
    return True  # For simplicity, always return True


def interpret_dsl(dsl_code):
    parse_tree = dsl_parser.parse(dsl_code)
    handle_statement(parse_tree)


# Example DSL code
dsl_code = """
if x {
    y
} else {
    z
}

while a {
    b
    c
}
"""

interpret_dsl(dsl_code)
