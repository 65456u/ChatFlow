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
# hello
flow origin {
    # Variables declared within the origin flow block
    assign "John" to name
    assign 25 to age

    # Start of a block
    {
        # Variable declared within the block
        assign "Smith" to lastName

        speak "Full name: " + name + " " + lastName
        speak "Age: " + age
    }  # End of the block

    # The following line will cause an error because lastName is not accessible here
    speak "Last name: " + lastName
}
"""


def create_my_speak(initial=0):
    def my_speak_function(message):
        nonlocal initial
        initial += 1
        print(initial, message)

    return my_speak_function


def main():
    interpreter = Interpreter(code=code)
    runtime = Runtime(interpreter, speak_function=create_my_speak())
    runtime.run()


if __name__ == "__main__":
    main()
