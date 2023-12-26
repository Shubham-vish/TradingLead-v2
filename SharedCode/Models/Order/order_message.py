from dataclasses import dataclass
from SharedCode.Models.Order.user_stoplosses import UserStoplosses, Stoploss, Constants as slConstants
from SharedCode.Models.user import User
from typing import Any, Optional, List
from SharedCode.Models.Order.order import Order
from typing import Union

@dataclass
class OrderConstants:
    order_type: str = "order_type"
    order_type_margin: str = "Margin"
    order_type_cnc: str = "CNC"
    order_type_stoploss: str = "Stoploss"

@dataclass
class OrderMessage:
    id: str
    user_id: str
    fyers_user_name: str
    kv_secret_name: str
    name: str
    order_type: str
    orders: Optional[Union[List[Order], List[Stoploss]]] = None
    
    
    @staticmethod
    def from_user_stoplosses(user_stoplosses:UserStoplosses, user:User)->'OrderMessage':
        return OrderMessage(user.user_id, user.user_id, user.fyers_user_name, user.kv_secret_name, user.name, OrderConstants.order_type_stoploss, user_stoplosses.stop_losses)