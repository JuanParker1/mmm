from datetime import datetime
from decimal import Decimal
from typing import Dict

from mmm.project_types import OrderType, Exchange


class Event:
    def __init__(self, data):
        self.raw_data = data


class TradesEvent(Event):

    def __init__(self, inst_id: str, price: Decimal, volume: Decimal, side: str, ts: datetime, origin_data: Dict):
        super(TradesEvent, self).__init__(origin_data)
        self.inst_id: str = inst_id
        self.price: Decimal = price
        self.volume: Decimal = volume
        self.side: str = side
        self.ts: datetime = ts

    def __repr__(self):
        return f"<inst_id: {self.inst_id}, price: {self.price}, volume: {self.volume}, " \
               f"side: {self.side}, ts: {self.ts}>"


class OrderBookEvent(Event):

    def __init__(self):
        """"""


class BarEvent(Event):

    def __init__(self):
        """"""


class Bar1MEvent(BarEvent):
    """"""


class OrderEvent(Event):
    """订单相关事件"""
    def __init__(self, exchange: "Exchange", order_type: "OrderType", params: dict, origin_data: Dict):
        super(OrderEvent, self).__init__(origin_data)
        self.exchange = exchange
        self.order_type = order_type
        self.params = params

    def __repr__(self):
        return f"<{self.order_type.name}|params: {self.params}>"












