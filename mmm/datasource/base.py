from typing import Dict, List

from mmm.events import Parser, Event


class DefaultParser(Parser):

    def parse(self, data: Dict) -> "Event" or List["Event"]:
        return Event(data)


class ParserFactory:
    def __init__(self):
        self.default_parser = DefaultParser()
        self.__registry__ = {}

    def get(self, channel: str) -> "Parser":
        return self.__registry__.get(channel, self.default_parser)

    def register(self, channel: str, parser: "Parser"):
        self.__registry__[channel] = parser

