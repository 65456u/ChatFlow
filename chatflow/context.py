class Context:
    """Context for a ChatFlow Flow

    This class represents the context for a ChatFlow flow. It stores information such as the flow's parameter,
    return value, scope, tree, and timeout status. It also provides methods for manipulating the scope and accessing
    variables within the scope.
    """

    def __init__(self, parameter, tree):
        """
        The constructor for the Context class.

        Args:
            parameter (any): The parameter used to passed to and from other flows.
            tree (lark.Tree): The tree representing the ChatFlow Flow.
        """
        self.parameter = parameter
        self.return_value = None
        self.scope = list()
        self.scope_count = 0
        self.tree = tree
        self.timeout = False

    def push_scope(self):
        """
        Pushes a new scope onto the stack.

        This method appends an empty dictionary to the `scope` list and increments the `scope_count` variable.

        """
        self.scope.append(dict())
        self.scope_count += 1

    def pop_scope(self):
        """
        Pops the topmost scope from the context.

        This method removes the topmost scope from the context's scope stack.

        """
        self.scope.pop()
        self.scope_count -= 1

    def get_variable(self, name):
        for i in range(self.scope_count - 1, -1, -1):
            if name in self.scope[i]:
                return self.scope[i][name]
        raise NameError(f"Name '{name}' is not defined")

    def set_variable(self, name, value):
            """Set the value of a variable in the context.

            Args:
                name (str): The name of the variable.
                value (Any): The value to assign to the variable.

            Returns:
                bool: True if the variable was successfully set, False otherwise.
            """
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
    
    def set_parameter(self, parameter):
        self.parameter = parameter
        
