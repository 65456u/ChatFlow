tributary_dict = {}


def register_tributary(script_name):
    def decorator(func):
        tributary_dict[script_name] = func
        return func

    return decorator


def get_tributary(name):
    return tributary_dict[name]


from .chatFlow import ChatFlow

__all__ = ["ChatFlow", "register_tributary"]
