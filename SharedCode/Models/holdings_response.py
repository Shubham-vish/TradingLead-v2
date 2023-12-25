from typing import List
from typing import Any
from dataclasses import dataclass
import json
from dataclasses import asdict
import math

@dataclass
class Holding:
    costPrice: float
    id: int
    symbol: str
    quantity: int
    segment: int
    pl: float
    ltp: float
    marketVal: float
    holdingType: str

    @staticmethod
    def from_dict(obj: Any) -> 'Holding':
        return Holding(
            costPrice=float(obj.get("costPrice")),
            id=int(obj.get("id")),
            symbol=str(obj.get("symbol")),
            quantity=int(obj.get("quantity")),
            segment=int(obj.get("segment")),
            pl=float(obj.get("pl")),
            ltp=float(obj.get("ltp")),
            marketVal=float(obj.get("marketVal")),
            holdingType=str(obj.get("holdingType"))
        )
        
    def to_dict(self) -> dict:
        return asdict(self)    

@dataclass
class Overall:
    count_total: int
    pnl_perc: float
    total_current_value: float
    total_investment: float
    total_pl: float

    @staticmethod
    def from_dict(obj: Any) -> 'Overall':
        _count_total = int(obj.get("count_total"))
        _pnl_perc = float(obj.get("pnl_perc"))
        _total_current_value = float(obj.get("total_current_value"))
        _total_investment = float(obj.get("total_investment"))
        _total_pl = float(obj.get("total_pl"))
        return Overall(_count_total, _pnl_perc, _total_current_value, _total_investment, _total_pl)
    
    
    def to_dict(self) -> dict:
        return asdict(self)    

@dataclass
class HoldingsResponse:
    code: int
    message: str
    s: str
    overall: Overall
    holdings: List[Holding]

    @staticmethod
    def from_dict(obj: Any) -> 'HoldingsResponse':
        _code = int(obj.get("code"))
        _message = str(obj.get("message"))
        _s = str(obj.get("s"))
        _overall = Overall.from_dict(obj.get("overall"))
        _holdings = [Holding.from_dict(y) for y in obj.get("holdings")]
        return HoldingsResponse(_code, _message, _s, _overall, _holdings)

    @staticmethod
    def from_json(json_string: str) -> 'HoldingsResponse':
        obj = json.loads(json_string)
        return HoldingsResponse.from_dict(obj)

    def to_dict(self) -> dict:
        return asdict(self)
    
    def get_quantity(self, ticker: str) -> int:
        for holding in self.holdings:
            if holding.symbol == ticker:
                return holding.quantity
        return 0
    
    def get_total_exposure(self) -> float:
        total_exposure = 0
        for holding in self.holdings:
            total_exposure += holding.quantity*holding.ltp
        return math.round(total_exposure, 2)
    
    def get_total_pl(self) -> float:
        total_pl = 0
        for holding in self.holdings:
            total_pl += holding.pl
        return math.round( total_pl, 2)
