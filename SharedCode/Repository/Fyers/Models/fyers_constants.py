class ProductType:
    cnc = "CNC"
    margin = "MARGIN"
    intraday = "INTRADAY"
    co = "CO"
    bo = "BO"


class OrderType:
    limit = 1
    market = 2
    stoploss_market = 3
    stoploss_limit = 4


class OrderSide:
    buy = 1
    sell = -1


class Response:
    OK = "ok"


class Constants:
    future_symbols = "FutureSymbolsAndLotSize"
