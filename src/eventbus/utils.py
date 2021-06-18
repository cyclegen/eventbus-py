import functools
import inspect


def get_class_that_defined_method(method):
    if isinstance(method, functools.partial):
        return get_class_that_defined_method(method.func)
    if inspect.ismethod(method) or (inspect.isbuiltin(method) and getattr(method, '__self__', None) is not None and getattr(method.__self__, '__class__', None)):
        for cls in inspect.getmro(method.__self__.__class__):
            if method.__name__ in cls.__dict__:
                return cls
        method = getattr(method, '__func__', method)  # fallback to __qualname__ parsing
    if inspect.isfunction(method):
        cls = getattr(inspect.getmodule(method),
                      method.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0],
                      None)
        if isinstance(cls, type):
            return cls
    return getattr(method, '__objclass__', None)  # handle special descriptor objects