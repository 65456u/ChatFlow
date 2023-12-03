import asyncio
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


code = """

"""


def create_my_speak(initial=0):
    def my_speak_function(message):
        nonlocal initial
        initial += 1
        print(initial, message)

    return my_speak_function

async def create_my_speak_async(initial=0):
    def my_speak_function(message):
        nonlocal initial
        initial += 1
        aprint(initial, message)

    return my_speak_function

async def main():
    interpreter = Interpreter(code=code)
    runtime = Runtime(interpreter)
    await runtime.arun()


if __name__ == "__main__":
    asyncio.run(main())