from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Repository.Fyers.fyers_service import FyersService
from dataclasses import asdict
from SharedCode.Models.Strategy.signal_message import SignalMessage
from SharedCode.Repository.CosmosDB.strategy_repository import StrategyRepository

telemetry = LoggerService()
kv_service = KeyVaultService()
strategy_repo = StrategyRepository()


def strategy_processor_runner(signal_message:SignalMessage, tel_props):
    tel_props = tel_props.copy()
    tel_props.update({"signal_message":asdict(signal_message), "user_id":signal_message.user_id, "action":"strategy_processor_runner"} )
    telemetry.info(f"Processing Strategy signal: {signal_message}", tel_props)
    
    if signal_message.to_do_something():
        if signal_message.to_buy():
            telemetry.info(f"Executing market buy: {signal_message}", tel_props)
            fyers_service = FyersService.from_kv_secret_name(signal_message.kv_secret_name, kv_service)
            fyers_service.place_buy_market(signal_message.trade_ticker, signal_message.get_quantity_to_buy(), signal_message.product_type, tel_props)
            telemetry.info(f"Executed market buy: {signal_message}", tel_props)
        elif signal_message.to_sell():
            telemetry.info(f"Executing market sell: {signal_message}", tel_props)
            fyers_service = FyersService.from_kv_secret_name(signal_message.kv_secret_name, kv_service)
            fyers_service.place_sell_market(signal_message.trade_ticker, signal_message.curr_quantity, signal_message.product_type, tel_props)
            telemetry.info(f"Executed market sell: {signal_message}", tel_props)
        try:
            strategy_repo.update_strategy_executed_for_user(signal_message)
        except Exception as e:
            telemetry.exception(f"Failed to update strategy_executed_for_user, Retry this manually: {signal_message}, error: {e}", tel_props)
    else:
        telemetry.exception(f"Nothing to do for signal, check why did this message even came to StrategyProcessor, it should not have come: {signal_message}", tel_props)
    
    
    