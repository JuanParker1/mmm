import asyncio
import logging
from events.event import Event
from events.event_source import EventSource, default_event_source_conf
from typing import Type, Dict, Callable


class StrategyMeta(type):
    def __new__(cls, name, bases, kwargs):  # noqa
        event_registry = {}
        schedule_plan = {}
        for method_name, method in kwargs.items():
            e = getattr(method, '__sub_event__', None)
            if e:
                event_registry[e] = method_name
            cron = getattr(method, '__schedule_plan__', None)
            if cron:
                schedule_plan[cron] = method_name

        kwargs['__event_registry__'] = event_registry
        kwargs['__schedule_plan__'] = schedule_plan
        return super().__new__(cls, name, bases, kwargs)


class Strategy(metaclass=StrategyMeta):
    __event_registry__: Dict[Type[Event], str] = {}
    __schedule_plan__: Dict[str, str] = {}


class StrategyRunner:
    def __init__(self, strategy: "Strategy", event_source_conf=default_event_source_conf):
        self.strategy = strategy
        self.event_source_conf = event_source_conf

    def create_schedule_task(self):
        registry = self.strategy.__schedule_plan__
        for plan, method_name in registry.items():


        async def schedule_task():
            ''''''

    def create_listen_tasks(self):
        async def _create_task(e: "EventSource", c: Callable):
            while True:
                event = await e.get()
                c(event)

        registry = self.strategy.__event_registry__
        for event_type, method_name in registry.items():
            event_source = self.event_source_conf.get(event_type, None)
            if event_source is None:
                logging.error(f'{event_type}没有对应的事件源')
            loop = asyncio.get_event_loop()
            method = getattr(self.strategy, method_name)
            loop.create_task(_create_task(event_source, method), name=f'{self.strategy}-wait-for-{event_type}-task')

    def create_tasks(self):
        self.create_listen_tasks()
        self.create_schedule_task()
