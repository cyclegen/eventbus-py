import inspect

from eventbus import subscribe
from eventbus.subscriber_method import SubscriberMethod


class Finder:

    def find(self, subscriber):
        return self._find_by_reflect(subscriber)

    def _find_by_reflect(self, subscriber):
        subscriber_methods = []

        methods = inspect.getmembers(subscriber, predicate=inspect.ismethod)
        for name, method in methods:
            annotation = getattr(method, subscribe.subscribe_annotation_property, None)
            if annotation is None:
                continue
            assert len(method.__annotations__) == 1, '订阅方法参数不合法'
            event_type = list(method.__annotations__.values())[0]
            subscriber_method = SubscriberMethod(method.__func__, event_type, priority=annotation.priority, sticky=annotation.sticky)
            subscriber_methods.append(subscriber_method)

        return subscriber_methods
