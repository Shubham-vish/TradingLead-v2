from dataclasses import dataclass
from SharedCode.Models.user_stoplosses import Stoploss, Constants as slConstants
from SharedCode.Utils.constants import Constants
from typing import Any, Optional
from dataclasses import asdict
from SharedCode.Models.order import Order

@dataclass
class OrderMessage:
    id: str
    user_id: str
    fyers_user_name: str
    kv_secret_name: str
    name: str
    is_stoploss: bool
    stoploss: Optional[Stoploss] = None
    order: Optional[Order] = None