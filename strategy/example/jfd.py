from events import TickerEvent, OrderBookEvent, default_event_source_conf
from events.event import OrderEvent, OrderAction
from strategy.base import Strategy
from strategy.decorators import sub_event, timer


class JfdStrategy(Strategy):

    def __init__(self, event_source_conf=default_event_source_conf):
        self.event_source_conf = event_source_conf

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
    def show(self):
        from datetime import datetime
        print(datetime.now())
        event_source = self.event_source_conf.get(OrderEvent)
        event_source.put_nowait(OrderEvent(OrderAction.CREATE_MARKET_ORDER, {'usdt': 100}))
