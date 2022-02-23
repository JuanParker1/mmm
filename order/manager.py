import logging

from events import default_event_source_conf
from events.event import OrderType, OrderEvent
from events.event_source import EventSourceConfig


class OrderManager:
    def __init__(self, event_source_conf: "EventSourceConfig" = default_event_source_conf):
        self.event_source = event_source_conf.get(OrderEvent)

    def _create_order(self, order_type, **kwargs):
        logging.info(f'下单：订单类型{order_type}, 参数: {kwargs}')
        sel

    def create_limit_order(self, **kwargs):
        return self._create_order(OrderType.LIMIT_ORDER, **kwargs)

    def create_market_order(self, **kwargs):
        return self._create_order(OrderType.MARKET_ORDER, **kwargs)

    ...


default_order_manager = OrderManager()
