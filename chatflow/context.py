class Context:
    def __init__(self, parameter, tree):
        self.parameter = parameter
        self.return_value = None
        self.scope = list()
        self.scope_count = 0
        self.tree = tree
        self.timeout = False

    def push_scope(self):
        self.scope.append(dict())
        self.scope_count += 1

    def pop_scope(self):
        self.scope.pop()
        self.scope_count -= 1

    def get_variable(self, name):
        for i in range(self.scope_count - 1, -1, -1):
            if name in self.scope[i]:
                return self.scope[i][name]
        return None

    def set_variable(self, name, value):
        for i in range(self.scope_count - 1, -1, -1):
            if name in self.scope[i]:
                self.scope[i][name] = value
                return False
        self.scope[self.scope_count - 1][name] = value
        return True

    def get_parameter(self):
        return self.parameter

    def set_timeout(self, timeout: bool):
        self.timeout = timeout

    def __repr__(self):
        return str(self.scope)
