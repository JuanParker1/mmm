from abc import ABC, abstractmethod


class OrderIDGenerator(ABC):
    @abstractmethod
    def gen(self): ...


class OkexOrderIDGenerator(OrderIDGenerator):
    def gen(self):
        pass


class BinanceOrderIDGenerator(OrderIDGenerator):
    def gen(self):
        pass
