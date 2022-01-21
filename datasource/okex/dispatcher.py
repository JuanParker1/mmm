from asyncio import Queue


class Dispatcher:
    def __init__(self):
        self.__register__ = {}

    def add_channel(self, channel_name: str, queue: "Queue"):
        self.__register__[channel_name] = queue

    def get_queue(self, channel_name: str) -> "Queue":
        try:
            return self.__register__[channel_name]
        except KeyError:
            raise RuntimeError(f'找不到{channel_name}对应的消息分发器')
