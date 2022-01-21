import asyncio
import json

from datasource.okex import OkexWsDatasource
from datasource.okex.dispatcher import Dispatcher
from queues import TickerQueue, OrderBooksQueue
from datasource.okex.parser import parser_factory

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
msg_dispatcher.add_channel('trades', TickerQueue)
msg_dispatcher.add_channel('books', OrderBooksQueue)


loop = asyncio.new_event_loop()
loop.create_task(OkexWsDatasource(parser_factory, msg_dispatcher).subscribe(topic1, TickerQueue), name='okex-ws-task')
loop.create_task(JfdStrategy(TickerQueue, OrderBooksQueue).run())
loop.run_forever()
