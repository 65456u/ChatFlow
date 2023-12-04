from chatflow import Interpreter, Runtime


class FlowTest:
    def __init__(self, user_input, expected_spoken):
        self.user_input = user_input
        self.expected_spoken = expected_spoken
        self.spoken = []

    def listen(self, timeout=None):
        print("heard", self.user_input[0])
        return self.user_input.pop(0)

    def speak(self, message):
        print("spoke", message)
        self.spoken.append(message)

    def judge(self):
        return self.expected_spoken == self.spoken


class ConversationScenario:
    def __init__(self, user_input, expected_spoken, code=None, code_path=None):
        self.code = code
        self.code_path = code_path
        self.test_suite = FlowTest(user_input, expected_spoken)

    def run(self):
        interpreter = Interpreter(code=self.code, code_path=self.code_path)
        runtime = Runtime(interpreter, self.test_suite.speak, self.test_suite.listen)
        runtime.run()
        return self.test_suite.judge()
