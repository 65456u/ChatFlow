class Runtime:
    def __init__(self, tree, speak_function, listen_function):
        self.tree = tree
        self.speak_function = speak_function
        self.listen_function = listen_function
        self.flow_dict = {}
        self.symbol_table = {}
        self.exit = False
        self.currentBlock = None
        for flow in self.tree.children:
            flow_name = flow.children[0].children[0].children[0]
            block = flow.children[1]
            self.flow_dict[flow_name] = block

    def run(self):
        self.currentBlock = self.flow_dict["origin"]
        while not self.exit and self.currentBlock is not None:
            self.run_block(self.currentBlock)

    def run_block(self, block):
        symbol_table = {}
        for statement in block.children:
            if self.exit:
                break
            self.run_statement(statement, symbol_table)

    def run_statement(self, statement, symbol_table):
        stmt = statement.children[0]
        match stmt.data:
            case "if_statement":
                self.run_if_statement(stmt, symbol_table)
            case "speak_statement":
                self.run_speak_statement(stmt, symbol_table)
            case "goto_statement":
                self.run_goto_statement(stmt, symbol_table)
            case "handover_statement":
                self.run_handover_statement(stmt, symbol_table)
            case "end_statement":
                self.run_end_statement(stmt)
            case "listen_statement":
                self.run_listen_statement(stmt, symbol_table)
            case "assign_statement":
                self.run_assign_statement(stmt, symbol_table)

    def run_if_statement(self, statement, symbol_table):
        condition = statement.children[0]
        result = self.evaluate_condition(condition, symbol_table)
        if result:
            self.run_block(statement.children[1])
        else:
            pass

    def run_speak_statement(self, statement, symbol_table):
        value = self.get_value(statement.children[0], symbol_table)
        self.speak_function(value)

    def run_goto_statement(self, statement, symbol_table):
        flow_name = statement.children[0].children[0].children[0]
        self.run_flow(flow_name)

    def get_value(self, tree, symbol_table):
        value = tree.children[0]
        match value.data:
            case "literal":
                return self.get_literal(value, symbol_table)
            case "identifier":
                return self.get_identifier_value(value, symbol_table)

    def get_identifier_value(self, tree, symbol_table):
        if tree.children[0] not in symbol_table:
            raise Exception("Variable not found")
        return symbol_table[tree.children[0]]

    def get_literal(self, tree, symbol_table):
        value = tree.children[0].value
        if type(value) == str:
            return value[1:-1]
        return value

    def run_handover_statement(self, statement, symbol_table):
        pass

    def run_end_statement(self, statement):
        self.exit = True

    def run_listen_statement(self, statement, symbol_table):
        match len(statement.children):
            case 1:
                value, timeout = self.listen_function()
                variable = statement.children[0].children[0].children[0]
                self.set_variable(variable, value, symbol_table)
            case 2:
                patient = self.get_timeout_value(statement.children[1], symbol_table)
                value, timeout = self.listen_function(patient)
                variable = statement.children[0].children[0].children[0]
                self.set_variable(variable, value, symbol_table)
            case 3:
                patient = self.get_timeout_value(statement.children[1], symbol_table)
                flow_name = statement.children[2].children[0].children[0]
                print(flow_name)
                value, timeout = self.listen_function(patient)
                if timeout:
                    self.run_flow(flow_name)
                else:
                    variable = statement.children[0].children[0].children[0]
                    self.set_variable(variable, value, symbol_table)

    def run_assign_statement(self, statement, symbol_table):
        pass

    def evaluate_condition(self, tree, symbol_table):
        condition_tree = tree.children[0]
        match condition_tree.data:
            case "match_compare":
                return self.evaluate_match_compare(condition_tree, symbol_table)
            case "equal_compare":
                return self.evaluate_equal_compare(condition_tree, symbol_table)
        return True

    def evaluate_match_compare(self, tree, symbol_table):
        print(tree)
        expression = self.get_value(tree.children[0], symbol_table)
        value = self.get_value(tree.children[1], symbol_table)
        return expression == value

    def evaluate_equal_compare(self, tree, symbol_table):
        left = self.get_value(tree.children[0], symbol_table)
        right = self.get_value(tree.children[1], symbol_table)
        return left == right

    def set_variable(self, variable, value, symbol_table):
        symbol_table[variable] = value

    def get_timeout_value(self, tree, symbol_table):
        timeout_value = int(tree.children[0].value)
        match tree.children[1].children[0].data:
            case "second":
                return timeout_value
            case "minute":
                return timeout_value * 60
            case "hour":
                return timeout_value * 60 * 60
