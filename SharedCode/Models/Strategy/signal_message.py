from dataclasses import dataclass
from SharedCode.Models.Strategy.strategy import StrategyUser


@dataclass
class SignalMessage:
    ticker:str
    trade_ticker:str
    user_id: str
    fyers_user_name: str
    kv_secret_name: str
    name: str
    strategy_name: str
    signal: int
    ltp: float
    product_type: str
    quantity:int
    
    
    @staticmethod
    def from_strategy_user(strategy_user:StrategyUser,  strategy_name: str, signal:bool, ltp:float )->'SignalMessage':
        return SignalMessage(strategy_user.ticker, strategy_user.trade_ticker, strategy_user.user_id, strategy_user.fyers_user_name, strategy_user.kv_secret_name, strategy_user.name, strategy_name, int(signal), ltp, strategy_user.product_type, strategy_user.quantity)