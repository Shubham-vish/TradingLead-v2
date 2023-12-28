from dataclasses import dataclass

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
    qty_t1:int