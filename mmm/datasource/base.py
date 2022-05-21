import logging
from typing import Dict, List

from mmm.events import Parser, Event


class DefaultParser(Parser):

    def parse(self, data: Dict) -> "Event" or List["Event"]:
        return Event(data)


class ParserFactory:
    def __init__(self):
        self.__register__ = {
            'default': DefaultParser()
        }

    def get_parser(self, channel: str) -> "Parser":
        try:
            return self.__register__[channel]
        except KeyError:
            logging.info(f'找不到{channel}对应的解析器, 返回默认解析器')
            return self.__register__['default']

    def add_parser(self, channel: str, parser: "Parser"):
        self.__register__[channel] = parser

