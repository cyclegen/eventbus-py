import logging
import typing

from eventbus.executor import MainOrderExecutor
from eventbus.finder import Finder
from eventbus.logger import Logger
from eventbus.subscription import Subscription


def get_default_logger(identifier):
    logger = logging.getLogger(f'EventBus[{identifier}]')
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger


class EventBus:

    def __init__(self, logger: Logger = None):
        self.finder = Finder()
        self.subscriptions_by_event_type: typing.Dict[type, typing.List[Subscription]] = {}
        self.event_types_by_subscriber: typing.Dict[object, typing.List[type]] = {}
        self.sticky_events: typing.Dict[type, object] = {}
        self.logger = logger if logger is not None else get_default_logger(id(self))
        self.executor = MainOrderExecutor(self)

    def register(self, subscriber):
        if self.is_registered(subscriber):
            self.logger.warning(f"{subscriber}已经注册过")
            return
        subscriber_methods = self.finder.find(subscriber)
        for subscriber_method in subscriber_methods:
            self.subscribe(subscriber, subscriber_method)

    def is_registered(self, subscriber) -> bool:
        return subscriber in self.event_types_by_subscriber

    def subscribe(self, subscriber, subscriber_method):
        event_type = subscriber_method.event_type
        subscription = Subscription(subscriber, subscriber_method)
        subscriptions = self.subscriptions_by_event_type.get(event_type, [])
        if subscription in subscriptions:
            raise Exception(f'订阅类{subscriber.__class__.__name__}已经注册了{event_type.__name__}事件')
        subscriptions.append(subscription)
        # 订阅方法重排序
        subscriptions.sort(key=lambda _subscription: _subscription.subscriber_method.priority)
        self.subscriptions_by_event_type.update({event_type: subscriptions})
        # 按照订阅者绑定事件类型
        subscriber_events = self.event_types_by_subscriber.get(subscriber, [])
        subscriber_events.append(event_type)
        self.event_types_by_subscriber.update({subscriber: subscriber_events})

        if subscriber_method.sticky:
            sticky_event = self.sticky_events.get(event_type, None)
            self.check_post_sticky_event_to_subscription(subscription, sticky_event)

    def check_post_sticky_event_to_subscription(self, subscription: Subscription, event):
        if event is not None:
            self.invoke_subscriber(subscription, event)

    def unregister(self, subscriber):
        subscribed_types = self.event_types_by_subscriber.get(subscriber)
        if subscribed_types is None:
            self.logger.warning(f"订阅者{subscriber}没有被正常注册故无需注销")
        else:
            for event_type in subscribed_types:
                self.unsubscribe_by_event_type(subscriber, event_type)

    def unsubscribe_by_event_type(self, subscriber, event_type):
        """按照事件类型取消订阅

        仅更新subscriptions_by_event_type,不更新types_by_subscriber，
        所以在调用该方法时必须提前调用更新types_by_subscriber
        :param subscriber:
        :param event_type:
        :return:
        """
        # 获取事件对应的subscription列表
        subscriptions = self.subscriptions_by_event_type.get(event_type, None)
        if subscriptions is None:
            return
        # 获取subscription列表中包含subscriber的元素
        for subscription in subscriptions:
            if subscription.subscriber == subscriber:
                # 失活状态
                subscription.active = False
                # 删除
                subscriptions.remove(subscription)

    def post(self, event):
        self.logger.info(f"正在发布事件{event}")
        subscriptions = self.subscriptions_by_event_type.get(event.__class__, [])
        for subscription in subscriptions:
            self.executor.enqueue(subscription, event)

    def post_sticky(self, event):
        self.sticky_events.update({event.__class__: event})
        self.post(event)

    def get_sticky_event(self, event_type):
        return self.sticky_events.get(event_type, None)

    def remove_sticky_event(self, event):
        """
        支持对事件类、事件实例进行解析并移除
        :param event: 事件类或事件实例
        :return:
        """
        if isinstance(event, type):
            del self.sticky_events[event]
        elif self.sticky_events.get(event.__class__) == event:
            del self.sticky_events[event.__class__]

    def cancel_delivery(self, event):
        setattr(event, '__cancelled__', True)
        if self.sticky_events.get(event.__class__) == event:
            self.remove_sticky_event(event)

    def invoke_subscriber(self, subscription, event):
        if subscription.active and not getattr(event, '__cancelled__', False):
            try:
                subscription.subscriber_method(subscription.subscriber, event)
            except Exception as exception:
                self.on_exception(subscription, event, exception)

    def on_exception(self, subscription, event, exception):
        self.logger.warning(f'在为{subscription}发送{event}时出现错误:{exception}')

    def stop(self):
        self.executor.stop()
