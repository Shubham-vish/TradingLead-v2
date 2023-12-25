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
    user_id = "UserId"
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

    @staticmethod
    def from_dict(obj: Any) -> 'Stoploss':
        
        _id = str(obj.get(Constants.id))
        _type = str(obj.get(Constants.type))
        
        if _type not in [Constants.type_normal, Constants.type_linear, Constants.type_trend]:
            raise ValueError("Invalid stoploss type")
        
        
        _ticker = str(obj.get(Constants.ticker))
        _price = float(obj.get(Constants.price))
        _product_type = str(obj.get(Constants.product_type))
        
        _trend_start = str(obj.get(Constants.trend_start, None))
        _trend_end = str(obj.get(Constants.trend_end, None))
        _check_at = str(obj.get(Constants.check_at, None))
        
        return Stoploss(_id, _type, _ticker, _price, _product_type, _trend_start, _trend_end, _check_at)
    
    def to_dict(self) -> dict:
        return asdict(self)

        
@dataclass
class UserStoplosses:
    user_id: str
    stop_losses: List[Stoploss]

    @staticmethod
    def from_json(json_string:str) -> 'UserStoplosses':
        return UserStoplosses.from_dict(json.loads(json_string))

    @staticmethod
    def from_dict(obj: Any) -> 'UserStoplosses':
        _user_id = str(obj.get(Constants.user_id))
        _stop_losses = [Stoploss.from_dict(y) for y in obj.get(Constants.stoplosses)]
        return UserStoplosses(_user_id,  _stop_losses)
    
    def to_dict(self) -> dict:
        stoplosses_dict = [stoploss.to_dict() for stoploss in self.stop_losses]
        return {
            Constants.id: self.user_id,
            Constants.user_id: self.user_id,
            Constants.stoplosses: stoplosses_dict
        }

    def get_normal_stoplosses(self) -> List[Stoploss]:
        normal_stoplosses = [stoploss for stoploss in self.stop_losses if stoploss.type == Constants.type_normal]
        return normal_stoplosses
    
    def get_stoplosses_dict(self) -> dict:
        stop_losses_dict = [stoploss.to_dict() for stoploss in self.stop_losses]
        return dict(stop_losses_dict)
    
    
# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)