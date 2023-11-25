
from .context import Context
from .runners import *


class Runtime:
    def __init__(self, tree, speak_function, listen_function):
        self.tree = tree
        self.speak_function = speak_function
        self.listen_function = listen_function
        self.flow_dict = {}
        self.symbol_table = {}
        self.exit = False
        self.register_flow()
        self.contextStack = []

    def register_flow(self):
        for flow in self.tree.children:
            flow_name = flow.children[0].children[0].children[0]
            block = flow.children[1]
            self.flow_dict[flow_name] = block

    def run(self):
        self.run_flow("origin")

    def run_flow(self, flow_name, parameter=None):
        if flow_name not in self.flow_dict:
            raise Exception(f"Flow {flow_name} not found")
        tree = self.flow_dict[flow_name]
        context = Context(parameter, tree)
        self.contextStack.append(context)
        self.run_block(tree, context)
        self.contextStack.pop()

    def run_block(self, block, context):
        context.push_scope()
        for statement in block.children:
            if self.exit:
                return
            self.run_statement(statement, context)

    def run_statement(self, statement, context):
        statement = statement.children[0]
        state_type = statement.data
        match state_type:
            case "speak_statement":
                self.run_speak(statement, context)
            case "listen_statement":
                self.run_listen(statement, context)
            case "if_statement":
                self.run_if(statement, context)
            case "engage_statement":
                self.run_engage(statement, context)
            case "assign_statement":
                run_assign(statement, context)
            case "end_statement":
                self.exit = True
            case "handover_statement":
                run_handover(statement, context)
            case "while_statement":
                self.run_while(statement, context)

    def run_speak(self, statement, context):
        value = get_expression(statement.children[0], context)
        self.speak_function(value)

    def run_listen(self, statement, context):
        length = len(statement.children)
        match length:
            case 1:
                value = self.listen_function()
                set_variable(statement.children[0], context, value)
            case 2:
                timer = get_time(statement.children[1], context)
                value = self.listen_function(timer)
                if value is None:
                    context.set_timeout(True)
                else:
                    set_variable(statement.children[0], context, value)

    def run_if(self, statement, context):
        condition = statement.children[0]
        result = get_condition(condition, context)
        if result:
            self.run_block(statement.children[1], context)
        else:
            if len(statement.children) == 3:
                self.run_else(statement.children[2], context)

    def run_else(self, statement, context):
        else_statement = statement.children[0]
        match else_statement.data:
            case "block":
                self.run_block(else_statement, context)
            case "if_statement":
                self.run_if(else_statement, context)

    def run_engage(self, statement, context):
        flow_name = get_flow_name(statement.children[0])
        self.run_flow(flow_name, context.get_parameter())

    def run_while(self, statement, context):
        condition = statement.children[0]
        while get_condition(condition, context):
            self.run_block(statement.children[1], context)
