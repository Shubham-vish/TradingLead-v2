from typing import List
from typing import Any
from dataclasses import dataclass
from SharedCode.Models.user import User
import json
from typing import Dict

@dataclass
class StrategyUser:
    user_id: str
    name: str
    email: str
    kv_secret_name: str
    fyers_user_name: str
    quantity: int
    curr_quantity: int
    ticker: str
    trade_ticker:str
    product_type: str
    
    
    @staticmethod
    def from_user(user: User, ticker: str, trade_ticker:str, quantity: int, curr_quantity:int, product_type: str)->'StrategyUser':
        return StrategyUser(user.id, user.name, user.email, user.kv_secret_name, user.fyers_user_name, quantity, ticker, trade_ticker, product_type)
        

    def is_in_trade(self):
        return self.curr_quantity >= self.quantity


@dataclass
class Strategy:
    id: str
    strategy_name: str
    strategy_details: Dict[str, Any]
    strategy_users: List[StrategyUser]
    _rid: str
    _self: str
    _etag: str
    _attachments: str
    _ts: int