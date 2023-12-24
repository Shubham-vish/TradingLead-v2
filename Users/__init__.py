from SharedCode.Repository.CosmosDB.user_repository import UserRepository
from SharedCode.Utils.constants import Constants
import azure.functions as func
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.utility import FunctionUtils
from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService

telemetry = LoggerService()

kv_service = KeyVaultService()
database_id = kv_service.get_secret(Constants.DATABASE_ID)
users_container_name = kv_service.get_secret(Constants.USERS_CONTAINER_NAME)
cosmos_db_service = CosmosDbService(database_id)
users_repo = UserRepository(cosmos_db_service, users_container_name)



def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    

    operation_id = FunctionUtils.get_operation_id(context)
    
    tel_props = {
        Constants.operation_id: operation_id,
        Constants.SERVICE: Constants.user_service,
        Constants.REQUEST_METHOD: req.method
    }
    
    telemetry.info('Python HTTP trigger for users started a request.', tel_props)

    if req.method == Constants.HTTP_POST:
        req_body = req.get_json()
        user_id = req_body.get('userId')
        email = req_body.get('email')
        name = req_body.get('name')

        tel_props.update( {
            'request': req.get_json(),
        })
        
        if user_id:
            users_repo.store_user(user_id, email, name, telemetry, tel_props)
            telemetry.info('User stored successfully.', tel_props)
            return func.HttpResponse("User stored successfully.", status_code=200)
        else:
            telemetry.exception('Invalid request body.', tel_props)
            return func.HttpResponse("Invalid request body.", status_code=400)
    else:
        telemetry.exception('Invalid request method.', tel_props)
        return func.HttpResponse("Invalid request method.", status_code=400)
