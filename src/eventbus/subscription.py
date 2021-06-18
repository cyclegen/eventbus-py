

class Subscription:

    def __init__(self, subscriber, subscriber_method):
        self.subscriber = subscriber
        self.subscriber_method = subscriber_method
        self.active = True

    def __eq__(self, other):
        if isinstance(other, Subscription):
            if other.subscriber == self.subscriber and other.subscriber_method == self.subscriber_method:
                return True
        return False

    def __str__(self):
        return f'<Subscription[{self.subscriber.__class__.__name__}@{hex(id(self.subscriber))} # {self.subscriber_method.method.__name__}@{hex(id(self.subscriber_method))}] at {hex(id(self))}>'