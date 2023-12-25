from typing import List, Optional
from typing import Any
from dataclasses import dataclass
import json
from dataclasses import asdict

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
    
    # Following are types of stoplosses 
    # and their check_at values
    check_at_closing = "closing"
    check_at_30t = "30t"
    check_at_hourly = "hourly"
    
    type_normal = "normal"
    type_linear = "line"
    type_trend = "trend"
    
@dataclass
class Stoploss:
    id: str
    type: str
    ticker: str
    price: float
    product_type: str
    trend_start: Optional[str] = None
    trend_end: Optional[str] = None
    check_at: Optional[str] = None

        
@dataclass
class UserStoplosses:
    id: str
    user_id: str
    stop_losses: List[Stoploss]

    def get_normal_stoplosses(self) -> List[Stoploss]:
        normal_stoplosses = [stoploss for stoploss in self.stop_losses if stoploss.type == Constants.type_normal]
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
    
# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)