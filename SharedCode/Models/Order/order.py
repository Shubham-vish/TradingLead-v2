from dataclasses import dataclass
from enum import Enum
from SharedCode.Models.Fyers.fyers_constants import OrderType, OrderSide, ProductType
@dataclass
class Order:
    symbol: str
    quantity: int
    price: float
    order_type: str
    side: str
    validity: str
    product_type: str
    trigger_price: float = 0.0
    stop_loss: float = 0.0
