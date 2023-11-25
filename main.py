from ChatFlow import ChatFlow
from inputimeout import inputimeout, TimeoutOccurred


def custom_input(timeout=None) -> tuple[str, bool]:
    try:
        if timeout:
            user_input = inputimeout(timeout=timeout)
        else:
            user_input = input()
        return user_input, False
    except TimeoutOccurred:
        return None, True


x = ChatFlow(print, custom_input, code_path="demo.flow")
x.run()
