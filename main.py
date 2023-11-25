from inputimeout import inputimeout, TimeoutOccurred

from ChatFlow import ChatFlow, register_tributary


def read_input_with_timeout(timeout=None):
    try:
        if timeout is None:
            user_input = input()
        else:
            user_input = inputimeout(timeout=timeout)
        return user_input
    except TimeoutOccurred:
        return None


@register_tributary("display")
def display(context):
    print(context)


@register_tributary("manual_service")
def manual_service(context):
    print("manual_service")


@register_tributary("comment_collector")
def comment_collector(context):
    print("comment_collector")


x = ChatFlow(print, read_input_with_timeout, code_path="example.flow")
x.run()
