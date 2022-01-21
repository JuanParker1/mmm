from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Dict, List

from events import TickerEvent


class ParserFactory:
    def __init__(self):
        self.__register__ = {}

    def get_parser(self, channel: str) -> "Parser":
        try:
            return self.__register__[channel]
        except KeyError:
            raise RuntimeError(f'找不到{channel}对应的解析器')

    def add_parser(self, channel: str, parser: "Parser"):
        self.__register__[channel] = parser


class Parser(ABC):

    @abstractmethod
    def parse(self, data: Dict): ...


class TickerParser(Parser):

    def parse(self, data: Dict) -> List[TickerEvent]:
        result = []
        data = data['data']
        for each in data:
            ticker = TickerEvent(each['instId'], Decimal(each['px']), Decimal(each['sz']), each['side'],
                                 datetime.fromtimestamp(int(each['ts'])/1000))
            result.append(ticker)
        return data


class OrderbookParser(Parser):

    def parse(self, data: Dict):
        return data  # todo


parser_factory = ParserFactory()
parser_factory.add_parser('trades', TickerParser())
parser_factory.add_parser('books', OrderbookParser())

















