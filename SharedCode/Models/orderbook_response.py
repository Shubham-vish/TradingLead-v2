from typing import List
from typing import Any
from dataclasses import dataclass
import json
@dataclass
class OrderBook:
    clientId: str
    id: str
    exchOrdId: str
    qty: int
    remainingQuantity: int
    filledQty: int
    discloseQty: int
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
    offlineOrder: bool
    orderDateTime: str
    orderValidity: str
    pan: str
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
    dqQtyRem: int
    orderNumStatus: str
    disclosedQty: int
    orderTag: str

@dataclass
class OrderBookResponse:
    s: str
    code: int
    message: str
    orderBook: List[OrderBook]

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
