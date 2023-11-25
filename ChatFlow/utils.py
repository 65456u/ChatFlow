from inputimeout import inputimeout, TimeoutOccurred


def replace_question_string(input_str, context):
    start_index = input_str.find("{")
    end_index = input_str.find("}")

    while start_index != -1 and end_index != -1:
        if start_index > 0 and input_str[start_index - 1] == "\\":
            start_index = input_str.find("{", start_index + 1)
            end_index = input_str.find("}", end_index + 1)
            continue

        variable_name = input_str[start_index + 1:end_index]
        value = context.get_variable(variable_name)
        if value is not None:
            input_str = input_str[:start_index] + str(value) + input_str[end_index + 1:]

        start_index = input_str.find("{", start_index + 1)
        end_index = input_str.find("}", end_index + 1)

    input_str = input_str.replace("\\{", "{").replace("\\}", "}")

    return input_str


def read_input_with_timeout(timeout=None):
    try:
        if timeout is None:
            user_input = input()
        else:
            user_input = inputimeout(timeout=timeout)
        return user_input
    except TimeoutOccurred:
        return None
