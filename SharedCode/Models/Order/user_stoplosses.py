from typing import List, Optional
from typing import Any
from dataclasses import dataclass
import json
from dataclasses import asdict
from dacite import from_dict
from enum import Enum
from SharedCode.Models.Fyers.fyers_constants import OrderType, OrderSide, ProductType

class Constants:
    type = "type"
    ticker = "ticker"
    price = "price"
    product_type = "product_type" 
    trend_start = "trend_start"
    trend_end = "trend_end"
    id = "id"
    stoplosses = "Stoplosses"
    check_at = "check_at"

class StoplossType(Enum):
    normal = "normal"
    line = "line"
    trend = "trend"

class StoplossCheckAt(Enum):
    closing = "closing"
    thirty_minute = "thirty_minute"
    hourly = "hourly"
    
@dataclass
class Stoploss:
    id: str
    ticker: str
    price: float
    qty: int
    type: StoplossType
    product_type: ProductType
    trend_start: Optional[str] = None
    trend_end: Optional[str] = None
    check_at: Optional[str] = None

        
@dataclass
class UserStoplosses:
    id: str
    user_id: str
    stop_losses: List[Stoploss]

    def get_normal_stoplosses(self) -> List[Stoploss]:
        normal_stoplosses = [stoploss for stoploss in self.stop_losses if stoploss.type == StoplossType.normal.value]
        return normal_stoplosses
    
    def get_30t_line_stoplosses(self) -> List[Stoploss]:
        normal_stoplosses = [stoploss for stoploss in self.stop_losses if stoploss.type == StoplossType.line.value and stoploss.check_at == StoplossCheckAt.thirty_minute.value]
        return normal_stoplosses
    
    def get_stoplosses_dict(self) -> dict:
        stop_losses_dict = [stoploss.to_dict() for stoploss in self.stop_losses]
        return dict(stop_losses_dict)
    
    def add_stoploss(self, stoploss: Stoploss):
        existing_stoploss = next((sl for sl in self.stop_losses if sl.id == stoploss.id), None)
        if existing_stoploss:
            existing_stoploss.__dict__ = stoploss.__dict__
        else:
            self.stop_losses.append(stoploss)

    def get_symbols_from_stoplosses(self):
        symbols = [stoploss.ticker for stoploss in self.stop_losses]
        return ",".join(symbols)
    
    def get_quote_dict(self):
        data = {
            "symbols": self.get_symbols_from_stoplosses()
        }
        return data

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)