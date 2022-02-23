import logging

from events import default_event_source_conf
from events.event import OrderType


class OrderManager:
    def __init__(self, event_source_conf=default_event_source_conf):
        self.event_source_conf = event_source_conf

    def _create_order(self, order_type, **kwargs):
        logging.info(f'下单：订单类型{order_type}, 参数: {kwargs}')

    def create_limit_order(self, **kwargs):
        return self._create_order(OrderType.LIMIT_ORDER, **kwargs)

    def create_market_order(self, **kwargs):
        return self._create_order(OrderType.MARKET_ORDER, **kwargs)

    ...


default_order_manager = OrderManager()
