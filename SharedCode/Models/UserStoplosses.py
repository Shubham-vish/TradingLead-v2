from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class Stoploss:
    type: str
    ticker: str
    price: float
    trend_start: str
    trend_end: str

    @staticmethod
    def from_dict(obj: Any) -> 'Stoploss':
        _type = str(obj.get("type"))
        _ticker = str(obj.get("ticker"))
        _price = float(obj.get("price"))
        _trend_start = str(obj.get("trendStart"))
        _trend_end = str(obj.get("trendEnd"))
        return Stoploss(_type, _ticker, _price, _trend_start, _trend_end)

@dataclass
class UserStoplosses:
    user_id: str
    fyers_user_name: str
    stop_losses: List[Stoploss]

    @staticmethod
    def from_dict(obj: Any) -> 'UserStoplosses':
        _user_id = str(obj.get("UserId"))
        _fyers_user_name = str(obj.get("FyersUserName"))
        _stop_losses = [Stoploss.from_dict(y) for y in obj.get("Stoplosses")]
        return UserStoplosses(_user_id, _fyers_user_name, _stop_losses)
    
    @staticmethod
    def from_json(json_string:str) -> 'UserStoplosses':
        return UserStoplosses.from_dict(json.loads(json_string))
    
    def get_normal_stoplosses(self) -> List[Stoploss]:
        normal_stoplosses = [stoploss for stoploss in self.stop_losses if stoploss.type == "normal"]
        return normal_stoplosses
    
    
# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)