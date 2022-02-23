import asyncio
import logging

from credential import Credential
from events import default_event_source_conf
from events.event import OrderEvent
from events.event_source import EventSourceConfig
from types import OrderType


def create_okex_order():
    """"""


class OrderExecutor:
    def __init__(self, event_source_conf: "EventSourceConfig" = default_event_source_conf):
        self.event_source_conf = event_source_conf
        self.event_source = event_source_conf.get(OrderEvent)
        if self.event_source is None:
            logging.error('OrderEvent没有对应的事件源')
        self.credential = Credential.load_from_env()

    def on_order(self, order: "OrderEvent"):
        if order.order_type == OrderType.LIMIT_ORDER:
            """创建现价单"""
            print(order)
        elif order.order_type == OrderType.MARKET_ORDER:
            """创建市价单"""
            print(order)
        ...

    def execute(self):

        async def _create_task():
            while True:
                event = await self.event_source.get()
                self.on_order(event)

        asyncio.get_event_loop().create_task(_create_task(), name=f'order-executor-wait-for-orderevent-task')  # noqa


default_order_executor = OrderExecutor()
