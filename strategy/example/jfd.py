from events import TickerEvent, OrderBookEvent
from strategy.base import Strategy
from strategy.decorators import sub_event, timer


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
    def show(self):
        from datetime import datetime
        print(datetime.now())
