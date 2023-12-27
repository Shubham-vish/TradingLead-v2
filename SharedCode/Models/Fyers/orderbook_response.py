from typing import List
from typing import Any
from dataclasses import dataclass
import json


@dataclass
class OrderStatus:
    filled = 2
    working = 6
    cancelled = 1
    rejected = 5

@dataclass
class OrderType:
    limit = 1
    market = 2
    stoploss_market = 3
    stoploss_limit = 4

@dataclass
class OrderBook:
    clientId: str
    id: str
    exchOrdId: str
    qty: int
    remainingQuantity: int
    filledQty: int
    limitPrice: float
    stopPrice: int
    tradedPrice: float
    type: int
    fyToken: str
    exchange: int
    segment: int
    symbol: str
    instrument: int
    message: str
    orderDateTime: str
    orderValidity: str
    productType: str
    side: int
    status: int
    source: str
    ex_sym: str
    description: str
    ch: float
    chp: float
    lp: float
    slNo: int
    disclosedQty: int
    orderTag: str

    def get_status(self) -> str:
        if self.status == 2:
            return "Filled"
        elif self.status == 6:
            return "Working"
        elif self.status == 1:
            return "Cancelled"
        elif self.status == 5:
            return "Rejected"
        else:
            return "Unknown"

@dataclass
class OrderBookResponse:
    s: str
    code: int
    message: str
    orderBook: List[OrderBook]

    def is_same_stoploss_present(self, ticker: str, qty: int) -> bool:
        for order in self.orderBook:
            if order.symbol == ticker and order.qty == qty and order.stopPrice != 0 and order.status == OrderStatus.working and (order.type == OrderType.stoploss_limit or order.type == OrderType.stoploss_market):
                return True
        return False

    def get_stoploss_orders_for_ticker(self, ticker: str) -> List[OrderBook]:
        return [order for order in self.orderBook if order.symbol == ticker and order.stopPrice != 0 and order.status == OrderStatus.working and (order.type == OrderType.stoploss_limit or order.type == OrderType.stoploss_market)]
# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
