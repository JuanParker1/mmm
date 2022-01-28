from abc import ABC, abstractmethod
from asyncio import Queue

from frozendict import frozendict

from .event import TickerEvent, OrderBookEvent, Bar1MEvent, Event


class EventSource(ABC):

    @abstractmethod
    async def put(self, event: "Event"):
        """"""

    @abstractmethod
    async def get(self) -> "Event":
        """"""


class AsyncioQueueEventSource(EventSource):

    def __init__(self, queue: Queue):
        self.queue = queue

    async def put(self, event: "Event"):
        self.queue.put_nowait(event)

    async def get(self):
        rv = await self.queue.get()
        self.queue.task_done()
        return rv


default_event_source_conf = frozendict({
    TickerEvent: AsyncioQueueEventSource(Queue(10000)),
    OrderBookEvent: AsyncioQueueEventSource(Queue(10000)),
    Bar1MEvent: AsyncioQueueEventSource(Queue(10000))
})

