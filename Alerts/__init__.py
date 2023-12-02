import json
import azure.functions as func
from SharedCode.Repository.CosmosDB.alerts_repository import AlertsRepository
from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils

import azure.functions as func

kv_service = KeyVaultService()
database_id = kv_service.get_secret(Constants.DATABASE_ID)
alerts_container_name = kv_service.get_secret(Constants.ALERTS_CONTAINER_NAME)
cosmos_db_service = CosmosDbService(database_id)
alerts_repo = AlertsRepository(cosmos_db_service, alerts_container_name)

telemetry = LoggerService()

application_json = "application/json"


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:

    operation_id = FunctionUtils.get_operation_id(context)
    
    tel_props = {
        Constants.operation_id: operation_id,
        Constants.SERVICE: Constants.holdings_service,
        Constants.REQUEST_METHOD: req.method
    }
    telemetry.info('Processing request to fetch user alerts.', tel_props)
    
    http_method = req.method
    user_id = req.route_params.get(Constants.REQUEST_PARAM_USER_ID)

    if http_method == Constants.HTTP_GET:
        alerts = alerts_repo.fetch_user_alerts(user_id, telemetry, tel_props)
        json_data = json.dumps(alerts)
        tel_props.update({Constants.RESPONSE_BODY: json_data})
        telemetry.info(f"Returnting Alerts for {user_id}", tel_props)
        return func.HttpResponse(json_data, mimetype=application_json, status_code=200)
    
    if http_method == Constants.HTTP_DELETE:
        try:
            req_body = req.get_json()
            tel_props.update({Constants.REQUEST_BODY: req_body})
            telemetry.info(f"Deleting Alerts for {user_id}", tel_props)
        except ValueError:
            telemetry.error("Invalid JSON", tel_props)
            return func.HttpResponse("Invalid JSON", status_code=400)

        ticker = req_body.get('ticker')

        if not ticker:
            json_response = json.dumps({"message": "Missing or empty value for ticker"})
            tel_props.update({Constants.RESPONSE_BODY: json_response})
            telemetry.error(json_response, tel_props)
            return func.HttpResponse(
                json_response,
                mimetype=application_json,
                status_code=400
            )

        alerts_repo.delete_user_alert(user_id, ticker, telemetry, tel_props)
        response_data = {
            "message": f"Alert deleted for {user_id} on ticker {ticker}",
        }
        json_response = json.dumps(response_data)
        tel_props.update({Constants.RESPONSE_BODY: json_response})
        return func.HttpResponse(json_response, mimetype="application/json", status_code=200)

    if http_method == Constants.HTTP_POST:
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse("Invalid JSON", status_code=400)

        user_id = req_body.get(Constants.REQUEST_PARAM_USER_ID)  # Replace this with actual user ID logic if needed
        trend_start = req_body.get('date1')
        trend_end = req_body.get('date2')
        ticker = req_body.get('ticker')
        stock_name = req_body.get('StockName')

        if not trend_start or not trend_end or not ticker:
            json_response = json.dumps({"message": "Missing or empty value for trend_start, trend_end or ticker"})
            tel_props.update({Constants.RESPONSE_BODY: json_response})
            telemetry.error(json_response, tel_props)
            return func.HttpResponse(
                json.dumps(json_response),
                mimetype=application_json,
                status_code=400
            )


        alerts_repo.create_user_alert(user_id, trend_start, trend_end, ticker, stock_name, telemetry, tel_props)
        
        response_data = {
            "message": f"Alert set for {user_id} on ticker {ticker} from {trend_start} to {trend_end}",
            "userId": user_id,
            "ticker": ticker,
            "trendStart": trend_start,
            "trendEnd": trend_end,
            "StockName": stock_name
        }
        json_response = json.dumps(response_data)
        tel_props.update({Constants.RESPONSE_BODY: json_response})
        telemetry.info(f"Returning Response after creating Alert for user: {user_id}", tel_props)
        return func.HttpResponse(json_response, mimetype="application/json", status_code=200)
