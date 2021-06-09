from eventbus import Subscribe, bus


class QuoteEvent:

    def __init__(self, data):
        self.open = data['open']
        self.high = data['high']
        self.low = data['low']
        self.close = data['close']


class OrderEvent:

    def __init__(self, symbol, price, amount):
        self.symbol = symbol
        self.price = price
        self.amount = amount


class TradeEvent:

    def __init__(self, symbol, price, amount):
        self.symbol = symbol
        self.price = price
        self.amount = amount


class TestSubscriber:

    def __init__(self):
        bus.get().register(self)

    @Subscribe()
    def on_event(self, event: QuoteEvent):
        print("开盘价: ", event.open)
        bus.get().post(OrderEvent('HUOBI.ETHUSDT', event.close, 200))


class StickyConfigEvent:

    def __init__(self, config):
        self.config = config


class StickySubscriber:

    def __init__(self):
        print('StickySubscriber will be registered')
        bus.get().register(self)

    @Subscribe(sticky=True)
    def call_by_sticky_event(self, event: StickyConfigEvent):
        print("粘滞事件配置: ", event.config)
        bus.get().remove_sticky_event(event)
        print('已移除粘滞事件')

    @Subscribe()
    def call_by_default_event(self, event: QuoteEvent):
        print("接受到行情数据，准备存入数据库: ", event.open)


class StickyNewSubscriber:

    def __init__(self):
        print('StickyNewSubscriber will be registered ')
        bus.get().register(self)

    @Subscribe(sticky=True)
    def call_by_sticky_event(self, event: StickyConfigEvent):
        print("若未移除则会有此条输出: ", event.config)

    @Subscribe()
    def call_by_default_event(self, event: QuoteEvent):
        print("接受到行情数据，准备存入数据库: ", event.open)


class SubscriberA:

    def __init__(self):
        bus.get().register(self)

    @Subscribe(priority=10)
    def on_event(self, event: OrderEvent):
        print(f'以价格{event.price}购买{event.symbol}共计{event.amount}')
        print(bus.get().subscriptions_by_event_type.get(OrderEvent, []))
        if len(bus.get().subscriptions_by_event_type.get(OrderEvent, [])) == 1:
                bus.get().stop()


class SubscriberB:

    def __init__(self):
        bus.get().register(self)

    @Subscribe(priority=100)
    def on_event(self, event: OrderEvent):
        print(f'已将{event.symbol}计入到资产组合')
        trade = TradeEvent(event.symbol, event.price, event.amount)

        print('还可以继续执行')
        bus.get().cancel_delivery(event)
        bus.get().post(trade)
        bus.get().unregister(self)


class SubscriberC:

    def __init__(self):
        # print(f'in subscriber c: {bus.get()}')
        bus.get().register(self)

    @Subscribe(priority=1)
    def on_event(self, event: TradeEvent):
        print(f"已撮合该交易: {event.symbol}-{event.price}-{event.amount}")
        order = OrderEvent(event.symbol, event.price, event.amount)
        bus.get().post(order)


def run():
    import random
    import string
    current_bus = bus.get()
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    setattr(current_bus, 'context_str', f'random_{salt}')
    test = TestSubscriber()
    SubscriberA()
    SubscriberB()
    SubscriberC()
    bus.get().post_sticky(StickyConfigEvent('模拟配置数据'))
    StickySubscriber()

    StickyNewSubscriber()
    bus.get().post(QuoteEvent({'open': 10, 'high': 100, 'low': 3, 'close': 60}))
    return test


if __name__ == '__main__':
    # from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
    # futures = []
    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     for i in range(10):
    #         futures.append(executor.submit(run))
    #
    # print([future.result() for future in futures])
    run()