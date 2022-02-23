from abc import ABC, abstractmethod
from asyncio import Queue
from typing import Type

from frozendict import frozendict

from .event import TickerEvent, OrderBookEvent, Bar1MEvent, Event, OrderEvent


class EventSource(ABC):

    @abstractmethod
    def put_nowait(self, event: "Event"):
        """"""

    @abstractmethod
    async def get(self) -> "Event":
        """"""


class AsyncioQueueEventSource(EventSource):

    def __init__(self, queue: Queue):
        self.queue = queue

    def put_nowait(self, event: "Event"):
        self.queue.put_nowait(event)

    async def get(self) -> "Event":
        rv = await self.queue.get()
        self.queue.task_done()
        return rv


class AsyncioQueueOrderEvent(EventSource):

    def __init__(self, queue: Queue):
        self.queue = queue

    def put_nowait(self, event: "Event"):
        self.queue.put_nowait(event)

    async def get(self) -> "Event":
        rv = await self.queue.get()
        self.queue.task_done()
        return rv


class EventSourceConfig:
    def __init__(self, kwargs):
        self._config = frozendict(kwargs)

    def get(self, event: Type[Event]):
        return self._config.get(event, None)


default_event_source_conf = EventSourceConfig({
    TickerEvent: AsyncioQueueEventSource(Queue(10000)),
    OrderBookEvent: AsyncioQueueEventSource(Queue(10000)),
    Bar1MEvent: AsyncioQueueEventSource(Queue(10000)),
    OrderEvent: AsyncioQueueOrderEvent(Queue(10000))
})
