import azure.functions as func
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
from SharedCode.Repository.CosmosDB.stoplosses_repository import StoplossesRepository
import azure.functions as func
from SharedCode.Runners.alerts_runner import alerts_runner

kv_service = KeyVaultService()

alerts_repo = StoplossesRepository()
telemetry = LoggerService()

application_json = "application/json"


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:

    operation_id = FunctionUtils.get_operation_id(context)
    
    tel_props = {
        Constants.operation_id: operation_id,
        Constants.SERVICE: Constants.alerts_service,
        Constants.REQUEST_METHOD: req.method,
        Constants.REQUEST_BODY: req.get_body()
    }
    
    telemetry.info(f'Processing request to fetch user alerts, {req.get_body()}', tel_props)

    response = alerts_runner(req, tel_props)
    
    telemetry.info(f'Returning response for request to fetch user alerts, {response.get_body()}', tel_props)
    
    return response
