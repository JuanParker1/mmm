import asyncio
import json

from datasource.okex import OkexWsDatasource
from datasource.okex.dispatcher import Dispatcher
from datasource.okex.parser import parser_factory
from events import ticker_event_source, orderbook_event_source
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

msg_dispatcher: "Dispatcher" = Dispatcher()
msg_dispatcher.add_channel('trades', ticker_event_source)
msg_dispatcher.add_channel('books', orderbook_event_source)

loop = asyncio.get_event_loop()
StrategyRunner(JfdStrategy()).create_tasks()
loop.create_task(OkexWsDatasource(parser_factory, msg_dispatcher).subscribe(topic1), name='okex-ws-task')
loop.run_forever()
