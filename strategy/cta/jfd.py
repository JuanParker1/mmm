import asyncio

from asyncio import Queue
from data import Ticker, OrderBook


class JfdStrategy:
    def __init__(self, ticker_queue: "Queue", orderbook_queue: "Queue"):
        self.ticker_queue = ticker_queue
        self.orderbook_queue = orderbook_queue

    def on_ticker(self, ticker: Ticker):
        """"""
        print(ticker)

    def on_order_book(self, order_book: OrderBook):
        """"""
        print(order_book)

    async def run(self):
        async def wait_for_ticker():
            while True:
                ticker = await self.ticker_queue.get()
                self.on_ticker(ticker)
                self.ticker_queue.task_done()

        async def wait_for_orderbook():
            while True:
                orderbook = await self.orderbook_queue.get()
                self.on_order_book(orderbook)
                self.orderbook_queue.task_done()
        loop = asyncio.get_running_loop()
        loop.create_task(wait_for_ticker(), name='jfdstrategy-wait-for-ticker-task')   # noqa
        loop.create_task(wait_for_orderbook(), name='jfdstrategy-wait-for-orderbook-task')  # noqa

