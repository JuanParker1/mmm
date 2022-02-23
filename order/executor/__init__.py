import asyncio
import logging

from credential import Credential
from events import default_event_source_conf
from events.event import OrderEvent
from types import OrderType


class OrderExecutor:
    def __init__(self, event_source_conf=default_event_source_conf):
        self.event_source_conf = event_source_conf
        self.credential = Credential.load_from_env()

    def on_order(self, order: "OrderEvent"):
        if order.action == OrderType.LIMIT_ORDER:
            """创建现价单"""
            print(order)
        elif order.action == OrderType.MARKET_ORDER:
            """创建市价单"""
            print(order)
        ...

    def execute(self):
        event_source = self.event_source_conf.get(OrderEvent, None)
        if event_source is None:
            logging.error('OrderEvent没有对应的事件源')

        async def _create_task():
            while True:
                event = await event_source.get()
                self.on_order(event)

        asyncio.get_event_loop().create_task(_create_task(), name=f'order-executor-wait-for-orderevent-task')  # noqa


default_order_executor = OrderExecutor()
