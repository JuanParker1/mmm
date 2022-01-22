import asyncio
import json

from datasource.okex import OkexWsDatasource
from datasource.okex.parser import parser_factory
from events import okex_dispatcher
from strategy import StrategyRunner
from strategy.cta.jfd import JfdStrategy

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


OkexWsDatasource(parser_factory, okex_dispatcher).subscribe(topic1)
StrategyRunner(JfdStrategy()).create_tasks()
asyncio.get_event_loop().run_forever()
