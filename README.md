### 加密货币量化交易框架mmm(make-more-money), 持续完善中

示例

```python
import asyncio
import json

from datasource.okex import OkexWsDatasource
from order.order_runner import default_order_runner
from events import TickerEvent, OrderBookEvent
from strategy.base import StrategyRunner
from strategy.base import Strategy
from strategy.decorators import sub_event, timer


class JfdStrategy(Strategy):

    @sub_event(TickerEvent)
    def on_ticker(self, ticker: TickerEvent):
        print(ticker)
        print('.' * 20)

    @sub_event(OrderBookEvent)
    def on_orderbook(self, order_book: OrderBookEvent):
        print(order_book)
        print('-' * 20)

    @timer(3)
    def schedule(self):
        from datetime import datetime
        print(datetime.now())
        self.order_manager.create_market_order(usdt=100)


if __name__ == '__main__':
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
```