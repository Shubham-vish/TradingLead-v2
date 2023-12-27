from typing import List
from typing import Any
from dataclasses import dataclass
import json
@dataclass
class Cmd:
    c: float
    h: float
    l: float
    o: float
    t: int
    tf: str
    v: int

@dataclass
class V:
    ask: float
    bid: float
    ch: float
    chp: float
    cmd: Cmd
    description: str
    exchange: str
    fyToken: str
    high_price: float
    low_price: float
    lp: float
    open_price: float
    original_name: str
    prev_close_price: float
    short_name: str
    spread: float
    symbol: str
    tt: str
    volume: int


@dataclass
class D:
    n: str
    s: str
    v: V


@dataclass
class TickerLtp:
    ticker: str
    ltp: float

@dataclass
class QuoteResponse:
    code: int
    d: List[D]
    message: str
    s: str

    def get_ticker_and_ltp(self) -> List[TickerLtp]:
        res = [ TickerLtp(d.v.symbol, d.v.lp) for d in self.d]
        return res
# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
