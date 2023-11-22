```
chatflow : (flow)+
flow : "flow" flow_name indent block dedent
statement : if_statement | speak_statement | goto_statement | handover_statement | end_statement | listen_statement
if_statement : "if" condition then indent block dedent (elif_statement)* else_statement?
elif_statement : elif condition indent block dedent
else_statement : else indent block dedent
block : statement*
speak_statement : "speak" message
goto_statement : "goto" flow_name
handover_statement : "handover" script_name
end_statement : "end"
listen_statement : "listen" "for" variable ("for" time "before" flow_name)?
condition : variable "match" pattern | variable "equals" pattern
variable : value | list
list : "[" value ("," value)* "]"
value : 

```

```
chatflow            ::= flow+
flow                ::= "flow" flow_name INDENT block DEDENT
statement           ::= if_statement | speak_statement | goto_statement | handover_statement | end_statement | listen_statement
if_statement        ::= "if" condition "then" INDENT block DEDENT (elif_statement)* else_statement?
elif_statement      ::= "elif" condition INDENT block DEDENT
else_statement      ::= "else" INDENT block DEDENT
block               ::= statement*
speak_statement     ::= "speak" message
goto_statement      ::= "goto" flow_name
handover_statement  ::= "handover" script_name
end_statement       ::= "end"
listen_statement    ::= "listen" "for" variable ("for" time "before" flow_name)?
condition           ::= variable "match" pattern | variable "equals" pattern | variable "larger" "than" variable | variable "less" "than" variable | not condition | condition "and" condition | condition "or" condition
variable            ::= identifier | literal | "["value (","value)*"]"
list                ::= "[" value ("," value)* "]"
literal : string_literal | integer_literal
asign_statement : "asign" variable "to" identifier
identifier : 
```

```
chatflow            ::= flow+
flow                ::= "flow" flow_name INDENT block DEDENT
statement           ::= if_statement | speak_statement | goto_statement | handover_statement | end_statement | listen_statement | asign_statement
if_statement        ::= "if" condition "then" INDENT block DEDENT (elif_statement)* else_statement?
elif_statement      ::= "elif" condition INDENT block DEDENT
else_statement      ::= "else" INDENT block DEDENT
block               ::= statement*
speak_statement     ::= "speak" message
goto_statement      ::= "goto" flow_name
handover_statement  ::= "handover" script_name
end_statement       ::= "end"
listen_statement    ::= "listen" "for" variable ("for" time "before" flow_name)?
condition           ::= variable "match" pattern | variable "equals" pattern | variable "larger" "than" variable | variable "less" "than" variable | "not" condition | condition "and" condition | condition "or" condition
variable            ::= identifier | literal | list
list                ::= "[" value ("," value)* "]"
literal             ::= string_literal | integer_literal
asign_statement     ::= "asign" variable "to" identifier
identifier          ::= <some_identifier>  ; Placeholder for identifier definition
value               ::= <some_value>  ; Placeholder for value definition
string_literal      ::= <some_string_literal>  ; Placeholder for string literal definition
integer_literal     ::= <some_integer_literal>  ; Placeholder for integer literal definition
flow_name           ::= <some_flow_name>  ; Placeholder for flow name definition
script_name         ::= <some_script_name>  ; Placeholder for script name definition
message             ::= <some_message>  ; Placeholder for message definition
pattern             ::= <some_pattern>  ; Placeholder for pattern definition
time                ::= <some_time>  ; Placeholder for time definition

```

```
chatflow            ::= flow+
flow                ::= "flow" flow_name INDENT block DEDENT
statement           ::= if_statement | speak_statement | goto_statement | handover_statement | end_statement | listen_statement | asign_statement
if_statement        ::= "if" condition "then" INDENT block DEDENT (elif_statement)* else_statement?
elif_statement      ::= "elif" condition INDENT block DEDENT
else_statement      ::= "else" INDENT block DEDENT
block               ::= statement*
speak_statement     ::= "speak" message
goto_statement      ::= "goto" flow_name
handover_statement  ::= "handover" script_name
end_statement       ::= "end"
listen_statement    ::= "listen" "for" variable ("for" time "before" flow_name)?
condition           ::= variable "match" pattern | variable "equals" pattern | variable "larger" "than" variable | variable "less" "than" variable | "not" condition | condition "and" condition | condition "or" condition
variable            ::= identifier | literal | list
list                ::= "[" value ("," value)* "]"
literal             ::= string_literal | integer_literal
asign_statement     ::= "asign" variable "to" identifier
identifier          ::= letter (letter | digit | "_")*
value               ::= identifier | literal | list
string_literal      ::= '"' (character - '"')* '"'
integer_literal     ::= digit+
flow_name           ::= identifier
script_name         ::= identifier
message             ::= string_literal
pattern             ::= string_literal
time                ::= integer_literal

```

```
newline : /(\r?\n[\t ]*)+/
indent
dedent
chatflow : flow+
flow : "flow" flowname newline indent block dedent
```

```
```

