import pytest

from chatflow import register_tributary
from suite import *


def while_test():
    expected_spoken = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    testCase = ConversationScenario([], expected_spoken, code_path="while_test.flow")
    result = testCase.run()
    assert result


def scope_test():
    user_input = []
    expected_spoken = ["spoke Full name: John Smith", "spoke Age: 25"]
    testCase = ConversationScenario(user_input, expected_spoken, code_path="scope_test.flow")
    with pytest.raises(NameError):
        testCase.run()


def engage_test():
    user_input = []
    expected_spoken = ["engaged"]
    testCase = ConversationScenario(user_input, expected_spoken, code_path="engage_test.flow")
    result = testCase.run()
    assert result


def branch_test():
    user_input = ["start"]
    expected_spoken = ["start"]
    testCase = ConversationScenario(user_input, expected_spoken, code_path="branch_test.flow")
    result = testCase.run()
    assert result
    user_input = ["final"]
    expected_spoken = ["final"]
    testCase = ConversationScenario(user_input, expected_spoken, code_path="branch_test.flow")
    result = testCase.run()
    assert result
    user_input = ["end"]
    expected_spoken = ["default"]
    testCase = ConversationScenario(user_input, expected_spoken, code_path="branch_test.flow")
    result = testCase.run()
    assert result


@register_tributary("test")
def tributary(context, speak_function, listen_function):
    speak_function("test")
    speak_function(context.get_parameter())


def handover_test():
    user_input = []
    expected_spoken = ["test", "para"]
    testCase = ConversationScenario(user_input, expected_spoken, code_path="handover_test.flow")
    result = testCase.run()
    assert result


def match_test():
    user_input = ["6633人"]
    expected_spoken = ["6633"]
    testCase = ConversationScenario(user_input, expected_spoken, code_path="match_test.flow")
    result = testCase.run()
    assert result


def main():
    while_test()
    scope_test()
    engage_test()
    branch_test()
    handover_test()
    match_test()


if __name__ == "__main__":
    main()
