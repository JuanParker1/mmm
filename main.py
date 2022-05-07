import asyncio
import json
import logging

from mmm.datasource import OkexWsDatasource
from mmm.order.order_runner import default_order_runner
from mmm.strategy.base import StrategyRunner
from mmm.events import TickerEvent, OrderBookEvent
from mmm.project_types import Exchange
from mmm.strategy.base import Strategy
from mmm.strategy.decorators import sub_event, timer


class JfdStrategy(Strategy):

    @sub_event(TickerEvent)
    def on_ticker(self, ticker: TickerEvent):
        """"""
        print(ticker)
        print('.'*20)

    @sub_event(OrderBookEvent)
    def on_orderbook(self, order_book: OrderBookEvent):
        """"""
        print(order_book)
        print('-'*20)

    @timer(3)
    def schedule(self):
        from datetime import datetime
        print(datetime.now())
        self.order_manager.create_market_order(Exchange.OKEX, usdt=100)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    topic1 = json.dumps({
        "op": "subscribe",
        "args": [{
            "channel": "trades",
            "instId": "BTC-USDT"
        }, {
            "channel": "books",
            "instId": "BTC-USDT"
        }]
    })
    OkexWsDatasource().subscribe(topic1)
    StrategyRunner(JfdStrategy()).create_tasks()
    default_order_runner.create_task()
    asyncio.get_event_loop().run_forever()
