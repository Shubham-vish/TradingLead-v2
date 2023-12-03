import datetime
import azure.functions as func
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
from TimerTriggerForAccessToken.access_token_generator_runner import access_token_generator_runner

telemetry = LoggerService()


def main(mytimer: func.TimerRequest, context: func.Context) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.access_token_generator_service,
        Constants.operation_id : operation_id,
    }
    
    telemetry.event(f'Python timer trigger function ran at {utc_timestamp}', tel_props)

    if mytimer.past_due:
        telemetry.info('The timer is past due!', tel_props)
    
    access_token_generator_runner(tel_props)

    