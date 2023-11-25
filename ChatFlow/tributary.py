tributary_dict = {}


def register_tributary(script_name):
    def decorator(func):
        tributary_dict[script_name] = func
        return func

    return decorator


def get_tributary(name):
    return tributary_dict[name]
