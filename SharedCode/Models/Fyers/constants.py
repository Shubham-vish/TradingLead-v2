from enum import Enum
from dataclasses import dataclass


@dataclass
class ProductType(Enum):
    CNC = "CNC"
    MARGIN = "MARGIN"
    INTRADAY = "INTRADAY"


@dataclass
class OrderType(Enum):
    limit = 1
    market = 2
    stoploss_market = 3
    stoploss_limit = 4


@dataclass
class OrderSide(Enum):
    buy = 1
    sell = -1


@dataclass
class Response:
    OK = "ok"


@dataclass
class Constants:
    future_symbols = "FutureSymbolsAndLotSize"
