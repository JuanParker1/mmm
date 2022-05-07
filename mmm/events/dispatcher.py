import asyncio.queues
import logging

from .event import Event
from .event_source import default_event_source_conf, EventSourceConfig


class Dispatcher:

    def __init__(self, event_source_conf: EventSourceConfig = default_event_source_conf):
        self.event_source_conf = event_source_conf

    async def dispatch(self, event: "Event"):
        event_source = self.event_source_conf.get(type(event))
        if event_source is None:
            raise RuntimeError(f'{event}找不到对应的事件源')
        try:
            event_source.put_nowait(event)
        except asyncio.queues.QueueFull:
            logging.error(event)


default_dispatcher = Dispatcher()
