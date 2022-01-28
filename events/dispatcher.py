from typing import Dict, Type

from .event import Event
from .event_source import default_event_source_conf, EventSource


class Dispatcher:

    def __init__(self, event_source_conf: Dict[Type["Event"], "EventSource"] = default_event_source_conf):
        self.event_source_conf = event_source_conf

    async def dispatch(self, event: "Event"):
        event_source = self.event_source_conf.get(type(event), None)
        if event_source is None:
            raise RuntimeError(f'{event}找不到对应的事件源')
        await event_source.put(event)


default_dispatcher = Dispatcher()
