from croniter import croniter
from datetime import datetime
from functools import wraps
from typing import Type
from events import Event


def schedule(cron: str, base=datetime.now()):
    # todo 检查plan合法性
    def new_func(func):
        @wraps(func)
        def wrap_func():
            return func()
        wrap_func.__schedule_plan__ = cron
        return wrap_func
    return new_func


def sub_event(event: Type[Event]):
    if not issubclass(event, Event):
        raise TypeError(f'sub_event参数必须是Event类型')

    def new_func(func):
        @wraps(func)
        def wrap_func(self, event_data):
            return func(self, event_data)
        wrap_func.__sub_event__ = event
        return wrap_func
    return new_func
