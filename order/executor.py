import asyncio
import logging

from credential import Credential
from events import default_event_source_conf
from events.event import OrderEvent
from events.event_source import EventSourceConfig
from types import OrderType
from third_party.okex.client import Client as OkexClient


class OrderExecutor:
    def __init__(self, credential: "Credential"):
        self.credential = credential


class OkexOrderExecutor:
    def __init__(self, credential: Credential):
        super().__init__(credential)
        self.client = OkexClient(credential.api_key, credential.secret_key, credential.phrase)

    def create_order(self, *args, **kwargs):
        pass


class BinanceOrderExecutor:
    def __init__(self, credential: Credential):
        super().__init__()



