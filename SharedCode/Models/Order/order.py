from dataclasses import dataclass

@dataclass
class Order:
    symbol: str
    quantity: int
    price: float
    order_type: str
    validity: str
    product_type: str
    trigger_price: float = 0.0
    stop_loss: float = 0.0
