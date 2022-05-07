from abc import ABC, abstractmethod
from mmm.credential import Credential
from mmm.order.utils import OkexOrderIDGenerator
from mmm.third_party.okex.client import Client as OkexClient


class OrderExecutor(ABC):
    def __init__(self, credential: "Credential"):
        self.credential = credential

    @abstractmethod
    def create_order(self, *args, **kwargs):
        pass

    @abstractmethod
    def query_order(self, client_order_id, timeout):
        pass


class OkexOrderExecutor(OrderExecutor):

    def __init__(self, credential: Credential):
        super().__init__(credential)
        self.client = OkexClient(credential.api_key, credential.secret_key, credential.phrase)
        self.order_id_generator = OkexOrderIDGenerator()

    def create_order(self, *args, **kwargs):
        client_order_id = self.order_id_generator.gen()
        # todo send order to exchange
        return client_order_id

    def query_order(self, client_order_id, timeout):
        # todo query order
        return client_order_id


class BinanceOrderExecutor:
    def __init__(self, credential: Credential):
        super().__init__()



