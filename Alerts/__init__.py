import logging
import json
from azure.cosmos import CosmosClient
import azure.functions as func
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from Repository.cosmos_db_repository import fetch_user_alerts, create_user_alert, update_user_alert, delete_user_alert



application_json = "application/json"


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    http_method = req.method
    user_id = req.route_params.get('userId')

    if http_method == "GET":
        alerts = fetch_user_alerts(user_id)
        return func.HttpResponse(json.dumps(alerts), mimetype=application_json, status_code=200)
    
    if http_method == "DELETE":
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse("Invalid JSON", status_code=400)

        ticker = req_body.get('ticker')

        if not ticker:
            return func.HttpResponse(
                json.dumps({"message": "Missing or empty value for ticker"}),
                mimetype=application_json,
                status_code=400
            )

        delete_user_alert(user_id, ticker)
        response_data = {
            "message": f"Alert deleted for {user_id} on ticker {ticker}",
        }
        return func.HttpResponse(json.dumps(response_data), mimetype="application/json", status_code=200)

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    user_id = req_body.get('userId')  # Replace this with actual user ID logic if needed
    trend_start = req_body.get('date1')
    trend_end = req_body.get('date2')
    ticker = req_body.get('ticker')
    stock_name = req_body.get('StockName')

    if not trend_start or not trend_end or not ticker:
        return func.HttpResponse(
            json.dumps({"message": "Missing or empty values for date1, date2, or ticker"}),
            mimetype=application_json,
            status_code=400
        )


    create_user_alert(user_id, trend_start, trend_end, ticker, stock_name)
    response_data = {
        "message": f"Alert set for {user_id} on ticker {ticker} from {trend_start} to {trend_end}",
        "userId": user_id,
        "ticker": ticker,
        "trendStart": trend_start,
        "trendEnd": trend_end,
        "StockName": stock_name
    }
    return func.HttpResponse(json.dumps(response_data), mimetype="application/json", status_code=200)
