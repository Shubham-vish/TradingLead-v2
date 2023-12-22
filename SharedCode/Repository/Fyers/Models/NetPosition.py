from typing import List
from typing import Any
from dataclasses import dataclass
import json
@dataclass
class NetPosition:
    symbol: str
    id: str
    buyAvg: float
    buyQty: int
    buyVal: float
    sellAvg: float
    sellQty: int
    sellVal: float
    netAvg: int
    netQty: int
    side: int
    qty: int
    productType: str
    realized_profit: float
    crossCurrency: str
    rbiRefRate: int
    fyToken: str
    exchange: int
    segment: int
    dayBuyQty: int
    daySellQty: int
    cfBuyQty: int
    cfSellQty: int
    qtyMulti_com: int
    pl: float
    unrealized_profit: int
    ltp: float
    slNo: int

    @staticmethod
    def from_dict(obj: Any) -> 'NetPosition':
        _symbol = str(obj.get("symbol"))
        _id = str(obj.get("id"))
        _buyAvg = float(obj.get("buyAvg"))
        _buyQty = int(obj.get("buyQty"))
        _buyVal = float(obj.get("buyVal"))
        _sellAvg = float(obj.get("sellAvg"))
        _sellQty = int(obj.get("sellQty"))
        _sellVal = float(obj.get("sellVal"))
        _netAvg = int(obj.get("netAvg"))
        _netQty = int(obj.get("netQty"))
        _side = int(obj.get("side"))
        _qty = int(obj.get("qty"))
        _productType = str(obj.get("productType"))
        _realized_profit = float(obj.get("realized_profit"))
        _crossCurrency = str(obj.get("crossCurrency"))
        _rbiRefRate = int(obj.get("rbiRefRate"))
        _fyToken = str(obj.get("fyToken"))
        _exchange = int(obj.get("exchange"))
        _segment = int(obj.get("segment"))
        _dayBuyQty = int(obj.get("dayBuyQty"))
        _daySellQty = int(obj.get("daySellQty"))
        _cfBuyQty = int(obj.get("cfBuyQty"))
        _cfSellQty = int(obj.get("cfSellQty"))
        _qtyMulti_com = int(obj.get("qtyMulti_com"))
        _pl = float(obj.get("pl"))
        _unrealized_profit = int(obj.get("unrealized_profit"))
        _ltp = float(obj.get("ltp"))
        _slNo = int(obj.get("slNo"))
        return NetPosition(_symbol, _id, _buyAvg, _buyQty, _buyVal, _sellAvg, _sellQty, _sellVal, _netAvg, _netQty, _side, _qty, _productType, _realized_profit, _crossCurrency, _rbiRefRate, _fyToken, _exchange, _segment, _dayBuyQty, _daySellQty, _cfBuyQty, _cfSellQty, _qtyMulti_com, _pl, _unrealized_profit, _ltp, _slNo)

@dataclass
class Overall:
    count_open: int
    count_total: int
    pl_realized: float
    pl_total: float
    pl_unrealized: int

    @staticmethod
    def from_dict(obj: Any) -> 'Overall':
        _count_open = int(obj.get("count_open"))
        _count_total = int(obj.get("count_total"))
        _pl_realized = float(obj.get("pl_realized"))
        _pl_total = float(obj.get("pl_total"))
        _pl_unrealized = int(obj.get("pl_unrealized"))
        return Overall(_count_open, _count_total, _pl_realized, _pl_total, _pl_unrealized)

@dataclass
class Root:
    code: int
    message: str
    s: str
    netPositions: List[NetPosition]
    overall: Overall

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _code = int(obj.get("code"))
        _message = str(obj.get("message"))
        _s = str(obj.get("s"))
        _netPositions = [NetPosition.from_dict(y) for y in obj.get("netPositions")]
        _overall = Overall.from_dict(obj.get("overall"))
        return Root(_code, _message, _s, _netPositions, _overall)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
