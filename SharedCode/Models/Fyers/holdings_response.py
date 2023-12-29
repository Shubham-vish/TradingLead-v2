from typing import List
from dataclasses import dataclass
import math
from SharedCode.Models.Fyers.holding import Holding


@dataclass
class Overall:
    count_total: int
    pnl_perc: float
    total_current_value: float
    total_investment: float
    total_pl: float


@dataclass
class HoldingsResponse:
    code: int
    message: str
    s: str
    overall: Overall
    holdings: List[Holding]

    def get_quantity(self, ticker: str) -> int:
        for holding in self.holdings:
            if holding.symbol == ticker:
                return holding.quantity
        return 0

    def get_total_exposure(self) -> float:
        total_exposure = 0
        for holding in self.holdings:
            total_exposure += holding.quantity * holding.ltp
        return math.round(total_exposure, 2)

    def get_total_pl(self) -> float:
        total_pl = 0
        for holding in self.holdings:
            total_pl += holding.pl
        return math.round(total_pl, 2)
