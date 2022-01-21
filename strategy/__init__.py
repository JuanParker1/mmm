import asyncio
from inspect import signature
from events import EventType, event_source_config


class StrategyMeta(type):
    def __new__(cls, name, bases, kwargs):  # noqa
        on_ticker = kwargs.get('on_ticker', None)
        kwargs['__on_ticker_implemented__'] = callable(on_ticker) and len(signature(on_ticker).parameters) == 2
        on_bar = kwargs.get('on_bar', None)
        kwargs['__on_bar_implemented__'] = callable(on_bar) and len(signature(on_bar).parameters) == 2
        on_orderbook = kwargs.get('on_orderbook', None)
        kwargs['__on_orderbook_implemented__'] = callable(on_orderbook) and len(signature(on_orderbook).parameters) == 2
        return super().__new__(cls, name, bases, kwargs)


class Strategy(metaclass=StrategyMeta):

    def on_bar(self, kline):
        """"""

    def on_ticker(self, ticker):
        """"""

    def on_orderbook(self, orderbook):
        """"""


class StrategyRunner:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def create_on_ticker_task(self):
        async def wait_for_ticker():
            s = event_source_config.get(EventType.TICKER)
            while True:
                ticker = await s.get()
                self.strategy.on_ticker(ticker)
                s.task_done()

        loop = asyncio.get_event_loop()
        loop.create_task(wait_for_ticker(), name=f'{self.strategy}-wait-for-ticker-task')

    def create_on_bar_task(self):
        async def wait_for_bar():
            s = event_source_config.get(EventType.BAR)
            while True:
                bar = await s.get()
                self.strategy.on_bar(bar)
                s.task_done()

        loop = asyncio.get_event_loop()
        loop.create_task(wait_for_bar(), name=f'{self.strategy}-wait-for-bar-task')

    def create_on_orderbook_task(self):
        async def wait_for_orderbook():
            s = event_source_config.get(EventType.ORDERBOOK)
            while True:
                orderbook = await s.get()
                self.strategy.on_orderbook(orderbook)
                s.task_done()

        loop = asyncio.get_event_loop()
        loop.create_task(wait_for_orderbook(), name=f'{self.strategy}-wait-for-orderbook-task')

    def create_tasks(self):
        if getattr(self.strategy, '__on_bar_implemented__'):
            self.create_on_bar_task()
        if getattr(self.strategy, '__on_ticker_implemented__'):
            self.create_on_ticker_task()
        if getattr(self.strategy, '__on_orderbook_implemented__'):
            self.create_on_orderbook_task()

