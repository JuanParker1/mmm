import asyncio
import functools
import inspect
import logging
import time
from inspect import signature

import schedule

from events import EventType, event_source_config


class StrategyMeta(type):
    def __new__(cls, name, bases, kwargs):  # noqa
        cls.check_on_ticker_impl(kwargs)
        cls.check_on_orderbook_impl(kwargs)
        cls.check_on_bar_impl(kwargs)
        return super().__new__(cls, name, bases, kwargs)

    @classmethod
    def check_on_ticker_impl(mcs, kwargs):
        on_ticker = kwargs.get('on_ticker', None)
        kwargs['__on_ticker_implemented__'] = callable(on_ticker) and len(signature(on_ticker).parameters) == 2

    @classmethod
    def check_on_orderbook_impl(mcs, kwargs):
        on_orderbook = kwargs.get('on_orderbook', None)
        kwargs['__on_orderbook_implemented__'] = callable(on_orderbook) and len(signature(on_orderbook).parameters) == 2

    @classmethod
    def check_on_bar_impl(mcs, kwargs):
        allowed_bar_type = (
            'on_bar_1m', 'on_bar_3m', 'on_bar_5m', 'on_bar_15m', 'on_bar_30m', 'on_bar_1h',
            'on_bar_2h', 'on_bar_4h', 'on_bar_6h', 'on_bar_8h', 'on_bar_12h', 'on_bar_1d',
            'on_bar_3d', 'on_bar_1w', 'on_bar_1month',
        )
        on_bar_method_impl = []
        for method_name, method in kwargs.items():
            if method_name.startswith('on_bar_'):
                if method_name not in allowed_bar_type:
                    logging.warning(f'{method_name}方法不属于有效的on_bar事件, '
                                    f'有效的on_bar事件为下面列表中的一个或多个:{allowed_bar_type}')
                if callable(method) and len(signature(method).parameters) == 2:
                    on_bar_method_impl.append(method_name[7:])
        kwargs['__on_bar_implemented__'] = on_bar_method_impl


def period(param):
    def f1(func):
        @functools.wraps(func)
        def f2(*args, **kwargs):
            return func(*args, **kwargs)
        f2.__schedule_period__ = param
        return f2
    return f1


class Strategy(metaclass=StrategyMeta):
    def on_bar_1m(self, kline):
        """"""

    def on_bar_3m(self, kline):
        """"""

    def on_bar_5m(self, kline):
        """"""

    def on_bar_15m(self, kline):
        """"""

    def on_bar_30m(self, kline):
        """"""

    def on_bar_1h(self, kline):
        """"""

    def on_bar_2h(self, kline):
        """"""

    def on_bar_4h(self, kline):
        """"""

    def on_bar_6h(self, kline):
        """"""

    def on_bar_8h(self, kline):
        """"""

    def on_bar_12h(self, kline):
        """"""

    def on_bar_1d(self, kline):
        """"""

    def on_bar_3d(self, kline):
        """"""

    def on_bar_1w(self, kline):
        """"""

    def on_bar_1month(self, kline):
        """"""

    def on_ticker(self, ticker):
        """"""

    def on_orderbook(self, orderbook):
        """"""

    @period('every(2).seconds')
    def on_timer(self):
        """按时间触发"""


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

    def create_on_bar_task(self, bar_type: str):
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

    def create_timer(self):
        period = self.strategy.on_timer.__schedule_period__  # noqa
        cmd_str = f"schedule.{period}.do(task)"
        exec(cmd_str, globals(), {'task': self.strategy.on_timer()})
        async def timer_task():
            def t():
                while True:
                    schedule.run_pending()
                    time.sleep(3)
            await asyncio.to_thread(t)
        asyncio.run_coroutine_threadsafe(timer_task(), asyncio.get_event_loop())

    def create_tasks(self):
        # if getattr(self.strategy, '__on_bar_implemented__'):
        #     on_bar_implemented = self.strategy
        #     self.create_on_bar_task()
        if getattr(self.strategy, '__on_ticker_implemented__'):
            self.create_on_ticker_task()
        if getattr(self.strategy, '__on_orderbook_implemented__'):
            self.create_on_orderbook_task()
        on_bar_implemented = getattr(self.strategy, '__on_bar_implemented__')
        for each in on_bar_implemented:
            each

