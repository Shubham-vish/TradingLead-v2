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

    @staticmethod
    def from_dict(obj: Any) -> 'OrderBook':
        _clientId = str(obj.get("clientId"))
        _id = str(obj.get("id"))
        _exchOrdId = str(obj.get("exchOrdId"))
        _qty = int(obj.get("qty"))
        _remainingQuantity = int(obj.get("remainingQuantity"))
        _filledQty = int(obj.get("filledQty"))
        _discloseQty = int(obj.get("discloseQty"))
        _limitPrice = float(obj.get("limitPrice"))
        _stopPrice = int(obj.get("stopPrice"))
        _tradedPrice = float(obj.get("tradedPrice"))
        _type = int(obj.get("type"))
        _fyToken = str(obj.get("fyToken"))
        _exchange = int(obj.get("exchange"))
        _segment = int(obj.get("segment"))
        _symbol = str(obj.get("symbol"))
        _instrument = int(obj.get("instrument"))
        _message = str(obj.get("message"))
        _offlineOrder = str(obj.get("offlineOrder"))
        _orderDateTime = str(obj.get("orderDateTime"))
        _orderValidity = str(obj.get("orderValidity"))
        _pan = str(obj.get("pan"))
        _productType = str(obj.get("productType"))
        _side = int(obj.get("side"))
        _status = int(obj.get("status"))
        _source = str(obj.get("source"))
        _ex_sym = str(obj.get("ex_sym"))
        _description = str(obj.get("description"))
        _ch = float(obj.get("ch"))
        _chp = float(obj.get("chp"))
        _lp = float(obj.get("lp"))
        _slNo = int(obj.get("slNo"))
        _dqQtyRem = int(obj.get("dqQtyRem"))
        _orderNumStatus = str(obj.get("orderNumStatus"))
        _disclosedQty = int(obj.get("disclosedQty"))
        _orderTag = str(obj.get("orderTag"))
        return OrderBook(_clientId, _id, _exchOrdId, _qty, _remainingQuantity, _filledQty, _discloseQty, _limitPrice, _stopPrice, _tradedPrice, _type, _fyToken, _exchange, _segment, _symbol, _instrument, _message, _offlineOrder, _orderDateTime, _orderValidity, _pan, _productType, _side, _status, _source, _ex_sym, _description, _ch, _chp, _lp, _slNo, _dqQtyRem, _orderNumStatus, _disclosedQty, _orderTag)

@dataclass
class OrderBookResponse:
    s: str
    code: int
    message: str
    orderBook: List[OrderBook]

    @staticmethod
    def from_dict(obj: Any) -> 'OrderBookResponse':
        _s = str(obj.get("s"))
        _code = int(obj.get("code"))
        _message = str(obj.get("message"))
        _orderBook = [OrderBook.from_dict(y) for y in obj.get("orderBook")]
        return OrderBookResponse(_s, _code, _message, _orderBook)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
