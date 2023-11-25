from ChatFlow import Interpreter, register_tributary

@register_tributary("display")
def display(context):
    print(context)


@register_tributary("manual_service")
def manual_service(context):
    print("manual_service")


@register_tributary("comment_collector")
def comment_collector(context):
    print("comment_collector")


x = Interpreter(code_path="example.flow")
x.run()
