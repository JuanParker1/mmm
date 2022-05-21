from datetime import datetime
from decimal import Decimal
from typing import Dict

from mmm.project_types import OrderType, Exchange


class Event:
    def __init__(self, data=None):
        self._raw_data = data

    @property
    def raw_data(self):
        return self._raw_data

    def __repr__(self):
        return str(self._raw_data)


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
        super(OrderBookEvent, self).__init__()


class BarEvent(Event):

    def __init__(self, bar_type: str, inst_id: str, ts: datetime, open_price: Decimal, high_price: Decimal, low_price: Decimal,
                 close_price: Decimal, volume: Decimal, volume_ccy: Decimal, origin_data: Dict):
        """
        :param volume: 交易量，以张为单位, 如果是衍生品合约，数值为合约的张数。如果是币币/币币杠杆，数值为交易货币的数量。
        :param volume_ccy: 交易量，以币为单位 如果是衍生品合约，数值为交易货币的数量。如果是币币/币币杠杆，数值为计价货币的数量。
        """
        super(BarEvent, self).__init__(origin_data)
        self.bar_type: str = bar_type
        self.inst_id: str = inst_id
        self.ts: datetime = ts
        self.open_price: Decimal = open_price
        self.high_price: Decimal = high_price
        self.low_price: Decimal = low_price
        self.close_price: Decimal = close_price
        self.volume: Decimal = volume
        self.volume_ccy: Decimal = volume_ccy


class OrderEvent(Event):
    """订单相关事件"""
    def __init__(self, exchange: "Exchange", order_type: "OrderType", params: dict):
        super(OrderEvent, self).__init__()
        self.exchange = exchange
        self.order_type = order_type
        self.params = params

    def __repr__(self):
        return f"<{self.order_type.name}|params: {self.params}>"












