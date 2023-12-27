from dataclasses import dataclass
from SharedCode.Models.Order.user_stoplosses import UserStoplosses, Stoploss, Constants as slConstants
from SharedCode.Models.user import User
from typing import Any, Optional, List
from SharedCode.Models.Order.order import Order
from typing import Union
from SharedCode.Models.fyers_constants import OrderType
from enum import Enum

@dataclass
class OrderSide(Enum):
    buy: str = "BUY"
    sell: str = "SELL"
    buy_stoploss: str = "BUY_STOPLOSS"

@dataclass
class OrderMessage:
    id: str
    user_id: str
    fyers_user_name: str
    kv_secret_name: str
    name: str
    order_side: OrderType
    orders: Optional[Union[List[Order], List[Stoploss]]] = None
    
    
    @staticmethod
    def from_stoplosses(stoplosses:List[Stoploss], user:User)->'OrderMessage':
        return OrderMessage(user.user_id, user.user_id, user.fyers_user_name, user.kv_secret_name, user.name, OrderSide.buy_stoploss, stoplosses)