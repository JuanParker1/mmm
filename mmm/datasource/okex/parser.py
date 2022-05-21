import logging
from datetime import datetime
from decimal import Decimal
from typing import Dict, List

from mmm.datasource.base import ParserFactory
from mmm.events import TradesEvent, OrderBookEvent, Event
from mmm.events.parser import Parser


class TradesParser(Parser):

    def parse(self, data: Dict) -> "TradesEvent" or List["TradesEvent"]:
        result = []
        data = data['data']
        for each in data:
            ticker = TradesEvent(each['instId'], Decimal(each['px']), Decimal(each['sz']), each['side'],
                                 datetime.fromtimestamp(int(each['ts'])/1000), data)
            result.append(ticker)
        return result


class OrderbookParser(Parser):

    def parse(self, data: Dict) -> "OrderBookEvent":
        return OrderBookEvent()  # todo


class DefaultParser(Parser):

    def parse(self, data: Dict) -> "Event" or List["Event"]:
        return data


parser_factory = ParserFactory()
parser_factory.add_parser('trades', TradesParser())
parser_factory.add_parser('books', OrderbookParser())

















