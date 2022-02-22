### 加密货币量化交易框架mmm(make-more-money)

示例

```python
import asyncio
import json

from datasource.okex import OkexWsDatasource
from order.executor import default_order_executor
from events import TickerEvent, OrderBookEvent
from strategy.base import StrategyRunner
from events.event import OrderEvent, OrderType
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
    def show(self):
        from datetime import datetime
        print(datetime.now())
        event_source = self.event_source_conf.get(OrderEvent)
        event_source.put_nowait(OrderEvent(OrderType.MARKET_ORDER, {'usdt': 100}))


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
    default_order_executor.execute()
    asyncio.get_event_loop().run_forever()
```