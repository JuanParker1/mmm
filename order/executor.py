import asyncio
import logging

from abc import ABC, abstractmethod
from credential import Credential
from events import default_event_source_conf
from events.event import OrderEvent
from events.event_source import EventSourceConfig
from order.utils import OkexOrderIDGenerator
from types import OrderType
from third_party.okex.client import Client as OkexClient


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
        pass


class BinanceOrderExecutor:
    def __init__(self, credential: Credential):
        super().__init__()



