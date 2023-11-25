from lark import Lark
from .runtime import Runtime

grammar = r"""
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

listen_statement: "listen" "for" variable ("for" time ("before" flow_name)? )?

assign_statement: "assign" identifier "to" expression

condition       : match_compare
                | equal_compare

match_compare   : expression "match" value ("as" variable)?

equal_compare  : expression "equals" expression

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

time_unit       : second | minute | hour

second          : "s"

minute          : "m"

hour            : "h"

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
tributary_dict = {}


def register_tributary(script_name):
    def decorator(func):
        tributary_dict[script_name] = func
        return func

    return decorator


class ChatFlow:
    def __init__(
        self,
        speak_function,
        listen_function,
        code_path=None,
        code=None,
    ):
        self.speak_function = speak_function
        self.listen_function = listen_function
        if code_path:
            with open(code_path, "r") as f:
                self.script = f.read()
        elif code:
            self.script = code
        self.parser = Lark(grammar, start="chatflow", parser="lalr")
        self.tree = self.parser.parse(self.script)

    def run(self):
        runtime = Runtime(self.tree, self.speak_function, self.listen_function)
        runtime.run()

    def __repr__(self):
        return self.tree.pretty()
