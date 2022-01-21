from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Ticker:
    """{"instId":"BTC-USDT","tradeId":"294661520","px":"42840.5","sz":"0.0002","side":"sell","ts":"1642690248179"}"""
    instId: str
    price: Decimal
    volume: Decimal
    side: str
    ts: datetime


@dataclass
class OrderBook:
    """
    {"arg":{"channel":"books","instId":"BTC-USDT"},"action":"update","data":[{"asks":[["43008","0.23291184","0","1"],["43226.8","0","0","0"]],"bids":[["42929.3","0.15","0","1"],["42928.3","0","0","0"],["42898.8","0.23291238","0","1"],["42554","0","0","0"]],"ts":"1642257060899","checksum":-295778431}]}
    """


