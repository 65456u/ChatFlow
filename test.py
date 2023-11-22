from lark import Lark
from lark import Transformer

grammar = """
chatflow        : flow+

flow            : "flow" flow_name "{" block "}"

block           : statement*

statement       : if_statement
                | speak_statement
                | goto_statement
                | handover_statement
                | end_statement
                | listen_statement
                | assign_statement

if_statement    : "if" condition "{" block "}" elif_statement* else_statement?
elif_statement  : "elif" condition "{" block "}"
else_statement  : "else" "{" block "}"

speak_statement : "speak" value

goto_statement  : "goto" flow_name

handover_statement : "handover" script_name

end_statement   : "end"

listen_statement: "listen" "for" variable ("for" time "before" flow_name)?

assign_statement: "assign" identifier "to" expression

condition       : expression "match" value ("as" variable)?
                | expression "equals" expression


expression      : term (add_sub_operator term)*

term            : factor (mul_div_operator factor)*

factor          : literal
                | identifier
                | "(" expression ")"

add_sub_operator: "+" | "-"

mul_div_operator: "*" | "/"

value           : literal
                | identifier

variable        : identifier

identifier      : IDENTIFIER_TOKEN

flow_name       : identifier

script_name     : identifier

time            : INTEGER_LITERAL time_unit

time_unit       : "s" | "m" | "h"

comparison_operator: "equals" | "larger" "than" | "less" "than"

literal         : STRING_LITERAL
                | NUMBER_LITERAL

IDENTIFIER_TOKEN: /[a-zA-Z_][a-zA-Z0-9_]*/
STRING_LITERAL  : /\"(\\.|[^"\n])*\"/
NUMBER_LITERAL  : SIGNED_NUMBER
INTEGER_LITERAL : INT

%import common.SIGNED_NUMBER
%import common.INT
%ignore /[\t\f\r ]/
%import common.NEWLINE -> NL
%ignore NL
%ignore /\/\/.*/
"""

# 读取语法定义文件
with open("dsl.lark", "r") as f:
    grammar = f.read()

with open("demo.flow", "r") as f:
    file_content = f.read()

# 创建解析器
parser = Lark(grammar, start="chatflow", parser="lalr")

# 解析输入
tree = parser.parse(file_content)

# 打印解析树
# print(tree.pretty())

flow_dict = {}
variable_dict = {}


def chatFlow(tree):
    for flow in tree.children:
        flow_register(flow)


def flow_register(tree):
    flow_name = tree.children[0]
    block = tree.children[1]
    flow_name_register(flow_name, block)


def flow_name_register(tree, block):
    register_identifier(tree.children[0], "flow", block)


def register_identifier(tree, category, data):
    identifier = tree.children[0].value
    match category:
        case "flow":
            if identifier in flow_dict:
                raise Exception("Duplicate flow name")
            flow_dict[identifier] = data
        case "variable":
            if identifier in variable_dict:
                raise Exception("Duplicate variable name")
            variable_dict[identifier] = data


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


chatFlow(tree)
run_flow("origin")