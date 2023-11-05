```
listen speak match
```

```
seg origin
	listen for question until 5
	if question match "人工" then
		goto manual
	elif question match "充值" then
		goto addup
seg manual
	handover customer_service
	call thank_procedure
seg addup
	speak "what's your number"
	listen for question match "\d+" as amount
	speak "are you trying to charge $amount yuan? (y for yes and n for no)"
	listen for question match [yn] as choice
	if choice equals "y"
		handover charge_procedure
	else
		speak "charge cancelled"
	call thank_procedure
seg thank_procedure
	speak "thank you"
	end
```

```
这个DSL样例包含了以下语法要点：

1. `seg`：定义一个段落，表示一个逻辑块的开始。
2. `listen for question until <次数>`：监听用户问题，最多等待指定次数的用户输入。
3. `if <条件> then`：如果条件满足，则执行后续操作。
4. `elif <条件> then`：如果前面的条件不满足，且当前条件满足，则执行后续操作。
5. `else`：如果前面的条件都不满足，则执行后续操作。
6. `goto <段落>`：跳转到指定的段落继续执行。
7. `handover <服务>`：转接到指定的服务或人员。
8. `call <段落>`：调用指定的段落进行处理。
9. `speak <内容>`：向用户输出指定的内容。
10. `listen for question match <模式> as <变量>`：监听用户输入，匹配指定的模式，并将匹配结果保存到指定的变量中。
11. `if <变量> equals <值>`：如果变量的值等于指定值，则执行后续操作。
12. `end`：表示脚本执行结束。

这些语法要点可以帮助定义问题匹配规则、转接服务、调用不同的段落，并根据用户输入执行相应的操作。根据具体的需求，你可以进一步扩展和定制DSL的语法规则。
```

````
以下是使用BNF（巴科斯范式）描述的DSL语法规则：

```
<program> ::= <segment>+

<segment> ::= "seg" <segment_name> <statement>+

<segment_name> ::= <identifier>

<statement> ::= <control_statement> | <action_statement>

<control_statement> ::= "if" <condition> "then" <segment_name>
                     | "elif" <condition> "then" <segment_name>
                     | "else"
                     | "goto" <segment_name>
                     | "handover" <service>
                     | "call" <segment_name>

<action_statement> ::= "speak" <string>
                     | "listen for question" ["until" <integer>]
                     | "listen for question" "match" <pattern> "as" <variable>

<condition> ::= <expression> <comparison_operator> <expression>

<expression> ::= <variable> | <string> | <integer>

<comparison_operator> ::= "equals"

<service> ::= <identifier>

<pattern> ::= <string>

<variable> ::= "$" <identifier>

<string> ::= "\"" <character>+ "\""

<identifier> ::= <letter> <letter_or_digit>*

<letter> ::= [a-zA-Z]

<letter_or_digit> ::= [a-zA-Z0-9]

<integer> ::= <digit>+

<digit> ::= [0-9]
```

上述BNF规则描述了DSL的基本语法结构，包括程序（`<program>`）、段落（`<segment>`）、控制语句（`<control_statement>`）、动作语句（`<action_statement>`）、条件（`<condition>`）、表达式（`<expression>`）、服务（`<service>`）、模式（`<pattern>`）、变量（`<variable>`）等的定义。你可以根据这些规则进行DSL解析和语法分析。请注意，这只是一个简化的示例，实际的DSL语法规则可能需要根据具体需求进行更详细和精确的定义。
````

