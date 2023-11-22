领域特定语言（Domain Specific Language，DSL）可以提供一种相对简单的文法，用于特定领域的业务流程定制。本作业要求定义一个领域特定脚本语言，这个语言能够描述在线客服机器人（机器人客服是目前提升客服效率的重要技术，在银行、通信和商务等领域的复杂信息系统中有广泛的应用）的自动应答逻辑，并设计实现一个解释器解释执行这个脚本，可以根据用户的不同输入，根据脚本的逻辑设计给出相应的应答。

下面是我设计的dsl的一个样例程序，用于处理用户的人工服务和充值请求，请你阅读并分析它

```
flow origin
	listen for question for 5s before timeouthandler
	if question match ["manul","fuck"] then
		goto manual
	elif question match "charge" then
		goto charge
	else
		goto unexplicitflow
		
flow timeouthandler 
	speak "time out"
	end

flow manual 
	handover customer_service
	call thank_flow

flow thank_flow 
	speak "thank you"
	end

flow charge
	speak "what's your number"
	listen for question for 5s before timeouthandler
	if question match "\d+" as amount
		speak f"r u trying to charge {amount} yuan?"
		listen for answer
		if answer equals "y"
			handover charge_procedure
	speak "charge cancelled"
	goto origin
```

```
<program> ::= <flow_definition>*
<flow_definition> ::= "flow" <flow_name> <flow_body>
<flow_body> ::= <statement>*
<statement> ::= <if_statement> | <goto_statement> | <end_statement> | <speak_statement> | <listen_statement> | <variable_assignment>
<if_statement> ::= "if" <condition> "then" <code_block>
<goto_statement> ::= "goto" <flow_name>
<end_statement> ::= "end"
<speak_statement> ::= "speak" <message>
<listen_statement> ::= "listen" "for" <input_type> "for" <timeout> "before" <timeout_handler>
<variable_assignment> ::= "if" <input_type> "match" <pattern> "as" <variable_name>
<condition> ::= <string_match> | <regex_match>
<string_match> ::= <string_literal> "match" <string_literal>
<regex_match> ::= <string_literal> "match" <regex_literal>
<input_type> ::= "question"
<message> ::= <string_literal>
<timeout> ::= <number_literal>
<timeout_handler> ::= <flow_name>
<pattern> ::= <string_literal>
<variable_name> ::= <identifier>
<flow_name> ::= <identifier>
<string_literal> ::= '"' <string_content> '"'
<string_content> ::= <any_sequence_of_characters_except_double_quote>
<regex_literal> ::= '/' <regex_content> '/'
<regex_content> ::= <any_sequence_of_characters_except_forward_slash>
<identifier> ::= <a_sequence_of_letters_and_digits_starting_with_letter>
<number_literal> ::= <a_sequence_of_digits>
```

