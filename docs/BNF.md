# BNF Definition of ChatFlow

Following is the BNF definition of ChatFlow:

```
chatflow         : flow+

flow             : "flow" flow_name "{" block "}"

block            : statement*

statement        : if_statement
                 | speak_statement
                 | engage_statement
                 | handover_statement
                 | end_statement
                 | listen_statement
                 | assign_statement
                 | while_statement
                 | store_statement
                 | fetch_statement
                 | "{" block "}"

store_statement  : "store" value

fetch_statement  : "fetch" variable

if_statement     : "if" condition "{" block "}" else_statement?

else_statement   : "else" "{" block "}"
                 | "else" if_statement

while_statement  : "while" condition "{" block "}"

speak_statement  : "speak" str_expression

str_expression   : value ( "+" value )*

engage_statement : "engage" flow_name

handover_statement : "handover" tributary_name

end_statement    : "end"

listen_statement : "listen" "for" variable ( "for" time )?

assign_statement : "assign" expression "to" variable

condition        : match_compare
                 | equal_compare
                 | larger_compare
                 | less_compare
                 | boolean
                 | timeout
                 | "not" condition

larger_compare   : expression "larger" "than" expression

less_compare     : expression "less" "than" expression 

boolean          : TRUE
                 | FALSE

TRUE             : "true"

FALSE            : "false"

match_compare    : expression "match" value ( "as" variable )?

equal_compare    : expression "equals" expression

expression       : term ( add_sub_operator term )*

term             : factor ( mul_div_operator factor )*

factor           : value
                 | "(" expression ")"

add_sub_operator : PLUS | MINUS

mul_div_operator : TIMES | DIVIDE

TIMES            : "*"

DIVIDE           : "/"

PLUS             : "+"

MINUS            : "-"

value            : timeout
                 | literal
                 | variable

variable         : identifier

identifier       : IDENTIFIER_TOKEN

flow_name        : identifier

tributary_name   : identifier

time             : value time_unit

time_unit        : second | minute | hour

second           : "s"

minute           : "m"

hour             : "h"

timeout          : "timeout"

comparison_operator : "equals" | "larger" "than" | "less" "than"

literal          : STRING_LITERAL
                 | NUMBER_LITERAL

IDENTIFIER_TOKEN : /[a-zA-Z_][a-zA-Z0-9_]*/
STRING_LITERAL   : /\"(\\.|[^"\n])*\"/
NUMBER_LITERAL   : SIGNED_NUMBER
```

