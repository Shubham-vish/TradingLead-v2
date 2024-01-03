import datetime

import azure.functions as func

import datetime

import azure.functions as func
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
from SharedCode.Models.Order.user_stoplosses import UserStoplosses, StoplossCheckAt
from ..SharedCode.Runners.stoploss_executor_runner import stoploss_executor_runner


telemetry = LoggerService()



def main(mytimer: func.TimerRequest,  context: func.Context) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.stoploss_executor_service,
        Constants.operation_id : operation_id,
    }
    
    if mytimer.past_due:
        telemetry.info('The timer is past due!', tel_props)

    telemetry.info(f'Timer trigger function StopLossExecutor started at {utc_timestamp}', tel_props)
    
    results = stoploss_executor_runner(StoplossCheckAt.thirty_minute , tel_props)
    
    telemetry.info(f"set_stoplosses_for_all_users completed with results: {results}", tel_props)
    
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    telemetry.info(f'Timer trigger function StopLossExecutor completed at {utc_timestamp}', tel_props)
