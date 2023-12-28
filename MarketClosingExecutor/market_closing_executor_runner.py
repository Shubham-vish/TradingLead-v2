from SharedCode.Models.Order.user_stoplosses import StoplossCheckAt
from StoplossExecutor.stoploss_executor_runner import stoploss_executor_runner
from SharedCode.Repository.Logger.logger_service import LoggerService

telemetry = LoggerService()
 
def market_closing_executor_runner(tel_props):
    
    results = stoploss_executor_runner(StoplossCheckAt.closing, tel_props)
    telemetry.info(f"market_closing_executor_runner completed with results: {results}", tel_props)
    return results