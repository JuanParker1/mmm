from asyncio import Queue
from enum import Enum


KlineQueue = Queue()
TickerQueue = Queue()
OrderBooksQueue = Queue()


class Event(Enum):
    TICKER = 1
    ORDERBOOK = 2
    KLINE = 3


class EventConfig:
    def __init__(self):
        self.__config__ = {}

    def register(self, event: Event, source: "Queue"):
        self.__config__[event] = source

    def get(self, event: Event):
        try:
            return self.__config__[event]
        except KeyError:
            raise RuntimeError(f'找不到{event}事件对应事件源')


event_config = EventConfig()
event_config.register(Event.TICKER, TickerQueue)
event_config.register(Event.ORDERBOOK, OrderBooksQueue)
event_config.register(Event.KLINE, KlineQueue)
