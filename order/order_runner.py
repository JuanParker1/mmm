import asyncio
import logging

from credential import Credential
from events import default_event_source_conf
from events.event import OrderEvent
from events.event_source import EventSourceConfig
from order.executor import OkexOrderExecutor, OrderExecutor, BinanceOrderExecutor
from types import Exchange


class OrderRunner:
    def __init__(self, event_source_conf: "EventSourceConfig" = default_event_source_conf):
        self.event_source_conf = event_source_conf
        self.event_source = event_source_conf.get(OrderEvent)
        if self.event_source is None:
            logging.error('OrderEvent没有对应的事件源')
        self.credential = Credential.load_from_env()
        self.cached_executor = {}

    def get_order_executor(self, exchange: "Exchange"):
        executor = self.cached_executor.get(exchange, None)
        if executor is None:
            if exchange == Exchange.OKEX:
                executor = OkexOrderExecutor(self.credential)
            elif exchange == Exchange.BINANCE:
                executor = BinanceOrderExecutor(self.credential)
        self.set_executor(exchange, executor)
        return executor

    def set_executor(self, exchange: "Exchange", executor: "OrderExecutor"):
        self.cached_executor[exchange] = executor

    async def on_order(self, order_event: "OrderEvent"):
        order_executor = self.get_order_executor(order_event.exchange)
        loop = asyncio.get_running_loop()
        client_order_id = await loop.run_in_executor(None, order_executor.create_order(order_event))

    def create_task(self):

        async def _create_task():
            while True:
                event = await self.event_source.get()
                await self.on_order(event)

        asyncio.get_event_loop().create_task(_create_task(), name=f'order-executor-wait-for-orderevent-task')  # noqa


default_order_runner = OrderRunner()
