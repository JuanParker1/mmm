import logging

from events import default_event_source_conf, EventSource
from events.event import OrderType, OrderEvent
from events.event_source import EventSourceConfig


class OrderManager:
    def __init__(self, event_source_conf: "EventSourceConfig" = default_event_source_conf):
        self.event_source: "EventSource" or None = event_source_conf.get(OrderEvent)
        if self.event_source is None:
            raise RuntimeError('OrderEvent事件源未配置！')

    def _create_order(self, order_type: "OrderType", **kwargs):
        logging.info(f'下单：订单类型{order_type}, 参数: {kwargs}')
        self.event_source.put_nowait(OrderEvent)

    def create_limit_order(self, **kwargs):
        return self._create_order(OrderType.LIMIT_ORDER, **kwargs)

    def create_market_order(self, **kwargs):
        return self._create_order(OrderType.MARKET_ORDER, **kwargs)

    ...


default_order_manager = OrderManager()
