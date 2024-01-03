import datetime
import azure.functions as func
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
from SharedCode.Runners.strategy_kernel_regression_runner import strategy_kernel_regression_runner


telemetry = LoggerService()

def main(mytimer: func.TimerRequest,  context: func.Context) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.strategy_executor_service,
        Constants.operation_id : operation_id,
    }
    
    if mytimer.past_due:
        telemetry.info('The timer is past due!', tel_props)

    telemetry.info(f'Timer trigger function StrategyExecutor started at {utc_timestamp}', tel_props)

    strategy_kernel_regression_runner(tel_props)
    
    telemetry.info(f'Timer trigger function StrategyExecutor completed at {utc_timestamp}', tel_props)