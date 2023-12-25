from dataclasses import dataclass

@dataclass
class Order:
    symbol: str
    quantity: int
    price: float
    order_type: str
    validity: str
    product_type: str
    disclosed_quantity: int = 0
    trigger_price: float = 0.0
    stop_loss: float = 0.0
    square_off: float = 0.0
    trailing_stop_loss: float = 0.0
