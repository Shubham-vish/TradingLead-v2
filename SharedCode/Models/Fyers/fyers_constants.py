from enum import Enum
from enum import Enum

class ProductType(Enum):
    CNC = "CNC"
    MARGIN = "MARGIN"
    INTRADAY = "INTRADAY"



class OrderType(Enum):
    limit = 1
    market = 2
    stoploss_market = 3
    stoploss_limit = 4


class OrderSide(Enum):
    buy = 1
    sell = -1


class Response:
    OK = "ok"


class Constants:
    future_symbols = "FutureSymbolsAndLotSize"
