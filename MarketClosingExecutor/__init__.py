import datetime

import azure.functions as func
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
from MarketClosingExecutor.market_closing_executor_runner import market_closing_executor_runner
telemetry = LoggerService()



def main(mytimer: func.TimerRequest, context: func.Context) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.market_start_executor_services,
        Constants.operation_id : operation_id,
    }
    
    if mytimer.past_due:
        telemetry.info('The timer is past due!', tel_props)

    telemetry.info(f'Timer trigger function MarketClosingExecutor started at {utc_timestamp}', tel_props)
    
    results = market_closing_executor_runner(tel_props)
    
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    telemetry.info(f'Timer trigger function MarketStartExecutor completed at {utc_timestamp} with results:{ results}', tel_props)

