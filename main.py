import asyncio
import json

from datasource.okex import OkexWsDatasource
from strategy.base import StrategyRunner
from strategy.example.jfd import JfdStrategy

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


# OkexWsDatasource().subscribe(topic1)
StrategyRunner(JfdStrategy()).create_tasks()
asyncio.get_event_loop().run_forever()
