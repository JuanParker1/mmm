from abc import ABC, abstractmethod
from asyncio import Queue
from datetime import datetime
from decimal import Decimal
from enum import Enum


class Event(ABC):

    @abstractmethod
    def get_event_type(self): ...


class TickerEvent(Event):

    def __init__(self, inst_id: str, price: Decimal, volume: Decimal, side: str, ts: datetime):
        self.inst_id: str = inst_id
        self.price: Decimal = price
        self.volume: Decimal = volume
        self.side: str = side
        self.ts: datetime = ts

    def get_event_type(self):
        return EventType.TICKER


class OrderBookEvent(Event):

    def __init__(self):
        """"""

    def get_event_type(self):
        return EventType.ORDERBOOK


class KlineEvent(Event):

    def __init__(self):
        """"""

    def get_event_type(self):
        return EventType.BAR


class EventSource(Queue):
    ...


class KlineEventSource(EventSource):
    """kline事件源"""


class TickerEventSource(EventSource):
    """ticker事件源"""


class OrderBooksEventSource(EventSource):
    """orderbook事件源"""


kline_event_source = KlineEventSource()
ticker_event_source = TickerEventSource()
orderbook_event_source = OrderBooksEventSource()

event_source_config = {
    EventType.BAR: kline_event_source,
    EventType.TICKER: ticker_event_source,
    EventType.ORDERBOOK: orderbook_event_source
}












