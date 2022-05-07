import logging

from mmm.events import default_event_source_conf, EventSource
from mmm.events.event import OrderType, OrderEvent
from mmm.events import EventSourceConfig
from mmm.project_types import Exchange


class OrderManager:
    def __init__(self, event_source_conf: "EventSourceConfig" = default_event_source_conf):
        self.event_source: "EventSource" or None = event_source_conf.get(OrderEvent)
        if self.event_source is None:
            raise RuntimeError('OrderEvent事件源未配置！')

    def _create_order(self, order_event: "OrderEvent"):
        logging.info(f'下单：订单类型{order_event.order_type}, 参数: {order_event.params}')
        self.event_source.put_nowait(order_event)

    def create_limit_order(self, exchange: "Exchange", **kwargs):
        order_event = OrderEvent(exchange, OrderType.LIMIT_ORDER, kwargs)
        return self._create_order(order_event)

    def create_market_order(self, exchange: "Exchange", **kwargs):
        order_event = OrderEvent(exchange, OrderType.MARKET_ORDER, kwargs)
        return self._create_order(order_event)

    ...


default_order_manager = OrderManager()
