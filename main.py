from chatflow import Interpreter, register_tributary, Runtime


@register_tributary("display")
def display(context, speak_function, listen_function):
    print(context)


@register_tributary("manual_service")
def manual_service(context, speak_function, listen_function):
    print("manual_service")


@register_tributary("comment_collector")
def comment_collector(context, speak_function, listen_function):
    print("comment_collector")


x = Interpreter(code_path="examples/example.flow")
y = Runtime(x)
y.run()
