from dataclasses import dataclass
from SharedCode.Models.user_stoplosses import Stoploss, Constants as slConstants
from SharedCode.Utils.constants import Constants
from typing import Any
from dataclasses import asdict

@dataclass
class StoplossMessage:
    id: str
    user_id: str
    fyers_user_name: str
    kv_secret_name: str
    name: str
    stoploss: Stoploss
    
    @staticmethod
    def from_dict(obj: Any) -> 'StoplossMessage':
        _id = str(obj.get(slConstants.id))
        _user_id = str(obj.get(slConstants.user_id))
        _fyers_user_name = str(obj.get(Constants.fyers_user_name))
        _kv_secret_name = str(obj.get(Constants.kv_secret_name))
        _name = str(obj.get("name"))
        _stoploss = Stoploss.from_dict(obj.get("stoploss"))
        
        return StoplossMessage(_id, _user_id, _fyers_user_name, _kv_secret_name, _name, _stoploss)
    
    def to_dict(self) -> dict:
        return asdict(self)