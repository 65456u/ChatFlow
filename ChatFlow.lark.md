ChatFlow.lark

```
start            : chatflow

chatflow         : flow+

flow             : "flow" NAME "{" block "}"

statement        : if_statement
                 | speak_statement
                 | goto_statement
                 | handover_statement
                 | end_statement
                 | listen_statement
                 | assign_statement

if_statement     : "if" condition"{" block "}" (elif_statement)* else_statement?
elif_statement   : "elif" condition "{" block "}"
else_statement   : "else" "{" block "}"

block            : statement*

speak_statement  : "speak" STRING_LITERAL

goto_statement   : "goto" NAME

handover_statement: "handover" NAME

end_statement    : "end"

listen_statement : "listen" "for" variable ("for" time "before" NAME)?

condition        : expression "match" pattern
                 | expression "equals" pattern
                 | expression "larger" "than" expression
                 | expression "less" "than" expression
                 | "not" condition
                 | condition "and" condition
                 | condition "or" condition

expression       : variable
                 | literal
                 | expression "+" expression
                 | expression "-" expression
                 | expression "*" expression
                 | expression "/" expression

variable         : variable_list

variable_list    : identifier ("," identifier)*

assignment       : variable_list "to" identifier

assign_statement  : "assign" assignment

identifier       : NAME

time             : /[0-9]+/ "s" | /[0-9]+/ "m" | /[0-9]+/ "h"

pattern_list     : pattern ("," pattern)*

pattern          : STRING_LITERAL | value_list

value_list       : "[" value ("," value)* "]"

list             : value_list

literal          : STRING_LITERAL
                 | NUMBER_LITERAL

value            : literal
                 | list


%import common.CNAME -> NAME
%import common.SIGNED_NUMBER -> NUMBER_LITERAL
%import common.ESCAPED_STRING -> STRING_LITERAL
%import common.WS -> WHITESPACE
%ignore WHITESPACE
%import common.NEWLINE -> NL
%ignore NL
%ignore "\n"
```

main.py

```
from lark import Lark
from lark import Transformer
# 读取语法定义文件
with open("ChatFlow.lark", "r") as f:
    grammar = f.read()

with open("test.flow", "r") as f:
    file_content = f.read()

# 创建解析器
parser = Lark(grammar, start="start", parser="lalr")

# 解析输入
tree = parser.parse(file_content)

# 打印解析树
print(tree.pretty())

```

