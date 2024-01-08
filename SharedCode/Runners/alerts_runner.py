import azure.functions as func
from SharedCode.Repository.Logger.logger_service import LoggerService
import types
from SharedCode.Repository.CosmosDB.stoplosses_repository import StoplossesRepository
from SharedCode.Utils.constants import Constants
import json
from SharedCode.Models.Order.user_stoplosses import Stoploss
import uuid


telemetry = LoggerService()
stoploss_repo = StoplossesRepository()
application_json = "application/json"

def process_delete_request(req, user_id, tel_props)-> func.HttpResponse:
    
    try:
        req_body = req.get_body()
        req_body = json.loads(req_body)
        tel_props.update({Constants.REQUEST_BODY: req_body})
        telemetry.info(f"Deleting Alerts for {user_id}", tel_props)
    except ValueError:
        telemetry.exception("Invalid JSON", tel_props)
        return func.HttpResponse("Invalid JSON", status_code=400)

    stoploss_id = req_body.get('stoploss_id')

    if not stoploss_id:
        json_response = json.dumps({"message": "Missing or empty value for stoploss_id"})
        telemetry.exception(json_response, tel_props)
        return func.HttpResponse(
            json_response,
            mimetype=application_json,
            status_code=400
        )

    stoploss_repo.delete_user_stoploss(user_id, stoploss_id, telemetry, tel_props)
    
    response_data = {
            "message": f"Alert deleted for {user_id} with id {stoploss_id}",
        }
    json_response = json.dumps(response_data)
    tel_props.update({Constants.RESPONSE_BODY: json_response})
    telemetry.info(f"Returning Response after deleting Alert for user: {user_id}", tel_props)
    response = func.HttpResponse(json_response, mimetype=application_json, status_code=200)
    return response
    

def process_get_request(user_id, tel_props)-> func.HttpResponse:
    alerts_and_stoploss = stoploss_repo.get_user_stoplosses(user_id, telemetry, tel_props)
    alerts = alerts_and_stoploss.get_alerts() if alerts_and_stoploss else []
    alerts_dict = [alert.to_dict() for alert in alerts]
    json_data = json.dumps(alerts_dict)
    tel_props.update({Constants.RESPONSE_BODY: json_data})
    telemetry.info(f"Returnting Alerts for {user_id}", tel_props)
    response = func.HttpResponse(json_data, mimetype=application_json, status_code=200)
    return response



def process_post_request(req, user_id, tel_props)-> func.HttpResponse:
    try:
        req_body = req.get_body()
        req_body = json.loads(req_body)
        tel_props.update({Constants.REQUEST_BODY: req_body})
        telemetry.info(f"Creating Alerts for {user_id}", tel_props)
    except ValueError:
        telemetry.exception("Invalid JSON", tel_props)
        return func.HttpResponse("Invalid JSON", status_code=400)
    
    ticker = req_body.get('ticker')
    
    if not req_body.get('id'):
        req_body['id'] = str(uuid.uuid4())
    
    req_body.setdefault('qty', 0)                
    req_body.setdefault('product_type', 'cnc')   

    stoploss = Stoploss(**req_body)
    stoploss_repo.store_user_stoplosses(user_id, stoploss, telemetry, tel_props)
    
    response_data = {
            "message": f"Alert set for {user_id} on ticker {ticker}",
            "user_id": user_id,
            "ticker": ticker,
            "alert": stoploss.to_dict()
        }
    
    json_response = json.dumps(response_data)
    tel_props.update({Constants.RESPONSE_BODY: json_response})
    telemetry.info(f"Returning Response after creating Alert for user: {user_id}", tel_props)
    response = func.HttpResponse(json_response, mimetype=application_json, status_code=200)
    return response


def alerts_runner(req: func.HttpRequest,  tel_props)-> func.HttpResponse :
    http_method = req.method
    user_id = req.route_params.get(Constants.REQUEST_PARAM_CORRECT_USER_ID)
    
    if user_id is None:
        telemetry.info(f"User ID not found in request params.", tel_props)
        return func.HttpResponse(
            "User ID not found in request params.",
            status_code=400
        )
    
    response = None
    if http_method == Constants.HTTP_GET:
        response = process_get_request(user_id, tel_props)
    
    if http_method == Constants.HTTP_DELETE:
        response = process_delete_request(req, user_id, tel_props)

    if http_method == Constants.HTTP_POST:
        response = process_post_request(req, user_id, tel_props)
    
    res_body = response.get_body().decode("utf-8")
    telemetry.info(f"Returning Response for request from alerts_runner, {res_body}", tel_props)
    return response
