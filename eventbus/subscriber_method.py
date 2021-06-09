import inspect

from eventbus.utils import get_class_that_defined_method


class SubscriberMethod:

    def __init__(self, method, event_type, priority: int = 0, sticky: bool = False):
        self.method = method
        self.event_type = event_type
        self.priority = priority
        self.sticky = sticky
        self.check_method_definition()

    def __call__(self, *args, **kwargs):
        self.method(*args, **kwargs)

    def __eq__(self, other):
        if self == other:
            return True
        elif isinstance(other, SubscriberMethod):
            self.check_method_definition()
            other.check_method_definition()
            return self.method_definition == other.method_definition
        else:
            return False

    def check_method_definition(self):
        class_name = get_class_that_defined_method(self.method).__name__
        method_name = self.method.__name__
        # todo: 消除潜在bug
        event_type = list(inspect.getfullargspec(self.method).annotations.values())[0].__name__
        self.method_definition = f'{class_name}#{method_name}({event_type})'

    def __repr__(self):
        return f'<SubscriberMethod: {self.method_definition}>'
