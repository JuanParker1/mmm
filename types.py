from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


@dataclass
class Asset:
    inst_id: str
    amount: Decimal


class OrderType(Enum):
    LIMIT_ORDER = 1
    MARKET_ORDER = 2
    ...


class Exchange(Enum):
    BINANCE = 1
    OKEX = 2
    ...
