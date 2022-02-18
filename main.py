import asyncio
import json

from datasource.okex import OkexWsDatasource
from order.executor import default_order_executor
from strategy.base import StrategyRunner
from strategy.example.jfd import JfdStrategy


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
