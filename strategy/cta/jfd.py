from events import TickerEvent, OrderBookEvent
from strategy import Strategy


class JfdStrategy(Strategy):

    def on_ticker(self, ticker: TickerEvent):
        """"""
        print(ticker)
        print('.'*20)

    def on_orderbook(self, order_book: OrderBookEvent):
        """"""
        print(order_book)
        print('-'*20)
