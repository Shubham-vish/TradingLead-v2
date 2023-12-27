from dataclasses import dataclass
from enum import Enum
from SharedCode.Models.fyers_constants import OrderType, OrderSide, ProductType
@dataclass
class Order:
    symbol: str
    quantity: int
    price: float
    order_type: OrderType
    side: OrderSide
    validity: str
    product_type: ProductType
    trigger_price: float = 0.0
    stop_loss: float = 0.0
