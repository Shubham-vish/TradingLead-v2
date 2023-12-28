import azure.functions as func
import datetime
import azure.functions as func
import datetime
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Repository.CosmosDB.stoplosses_repository import StoplossesRepository
from SharedCode.Utils.constants import Constants
from SharedCode.Models.Order.user_stoplosses import UserStoplosses
from SharedCode.Repository.CosmosDB.user_repository import UserRepository
import concurrent.futures
import json
from SharedCode.Models.Order.order_message import OrderMessage
from SharedCode.Repository.ServiceBus.servicebus_service import ServiceBusService
from dataclasses import asdict
from SharedCode.Models.Order.user_stoplosses import UserStoplosses, Stoploss
from SharedCode.Models.user import User
from SharedCode.Repository.Fyers.fyers_service import FyersService
from SharedCode.Models.Fyers.holdings_response import HoldingsResponse
from SharedCode.Models.Fyers.net_positions_response import NetPositionResponse
from SharedCode.Models.Fyers.quote_response import QuoteResponse, TickerLtp
from typing import List
from SharedCode.Models.Order.user_stoplosses import StoplossCheckAt
from SharedCode.Utils.utility import FunctionUtils
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Repository.CosmosDB.user_repository import UserRepository
from SharedCode.Repository.ServiceBus.servicebus_service import ServiceBusService
from SharedCode.Repository.Cache.redis_cache_service import RedisCacheService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
import os
import pandas as pd
import io
import csv

from SharedCode.Repository.CosmosDB.alerts_repository import AlertsRepository
from SharedCode.Repository.CosmosDB.holdings_repository import HoldingsRepository
from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from Runners.stoploss_executor_runner import stoploss_executor_runner
from Runners.access_token_generator_runner import access_token_generator_runner
from Runners.plot_trendline_runner import generate_chart
from Runners.order_executor_runner import order_executor_runner
from Runners.market_start_executor_runner import market_start_executer_runner
from Runners.market_closing_executor_runner import market_closing_executor_runner
from Runners.fetch_store_stock_history_data_runner import fetch_store_history_data_runner

from Runners.fetch_store_participants_data_runner import fetch_store_data_for_n_days

kv_service = KeyVaultService()
telemetry = LoggerService()
user_repository = UserRepository()
sb_service = ServiceBusService()

database_id = kv_service.get_secret(Constants.DATABASE_ID)
holding_container_name = kv_service.get_secret(Constants.HOLDINGS_CONTAINER_NAME)
cosmos_db_service = CosmosDbService(database_id)
holdings_repo = HoldingsRepository(cosmos_db_service, holding_container_name)
alerts_container_name = kv_service.get_secret(Constants.ALERTS_CONTAINER_NAME)
alerts_repo = AlertsRepository(cosmos_db_service, alerts_container_name)

app = func.FunctionApp()


# Executes Orders
@app.service_bus_topic_trigger(arg_name="message", subscription_name="executor", topic_name="orders",
                               connection="sbtradinglead_SERVICEBUS") 
def OrderExecutor(message: func.ServiceBusMessage, context: func.Context) -> None:
    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.order_executor_service,
        Constants.operation_id : operation_id,
    }
    
    telemetry.info(f"StopLoss Executor ServiceBus trigger function processing message: {message}", tel_props)
    message_body = message.get_body().decode("utf-8")
    json_message = json.loads(message_body)
    
    tel_props.update({"message":json_message})
    order_message = OrderMessage(**json_message)
    
    telemetry.info(f"StopLoss Executor ServiceBus parsed message properly: {json_message}", tel_props)
    
    order_executor_runner(order_message, tel_props)
    
    telemetry.info(f"StopLoss Executor ServiceBus trigger function processed message: {message}", tel_props)


# Timmer Trigger for Strategy and Order Execution
# -------------------------------
# -------------------------------
# -------------------------------
# -------------------------------
@app.timer_trigger(schedule="0 10,40 4,5,6,7,8,9,10 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def stoploss_executor(myTimer: func.TimerRequest, context: func.Context) -> None:
    
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.stoploss_executor_service,
        Constants.operation_id : operation_id,
    }
    
    if myTimer.past_due:
        telemetry.info('The timer is past due!', tel_props)

    telemetry.info(f'Timer trigger function stoploss_executor started at {utc_timestamp}', tel_props)
    
    results = stoploss_executor_runner(StoplossCheckAt.thirty_minute , tel_props)
    
    telemetry.info(f"set_stoplosses_for_all_users completed with results: {results}", tel_props)
    
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    telemetry.info(f'Timer trigger function stoploss_executor completed at {utc_timestamp}', tel_props)
    
    

@app.timer_trigger(schedule="0 25 10 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def MarketClosingExecutor(myTimer: func.TimerRequest, context: func.Context) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.market_start_executor_services,
        Constants.operation_id : operation_id,
    }
    
    if myTimer.past_due:
        telemetry.info('The timer is past due!', tel_props)

    telemetry.info(f'Timer trigger function MarketClosingExecutor started at {utc_timestamp}', tel_props)
    
    results = market_closing_executor_runner(tel_props)
    
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    telemetry.info(f'Timer trigger function MarketStartExecutor completed at {utc_timestamp} with results:{ results}', tel_props)
    
    

@app.timer_trigger(schedule="0 40 4 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def MarketStartExecutor(myTimer: func.TimerRequest, context: func.Context) -> None:
    
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.market_start_executor_services,
        Constants.operation_id : operation_id,
    }
    
    if myTimer.past_due:
        telemetry.info('The timer is past due!', tel_props)

    telemetry.info(f'Timer trigger function MarketStartExecutor started at {utc_timestamp}', tel_props)
    
    results = market_start_executer_runner(tel_props)
    
    telemetry.info(f"set_stoplosses_for_all_users completed with results: {results}", tel_props)
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    telemetry.info(f'Timer trigger function MarketStartExecutor completed at {utc_timestamp} with results:{ results}', tel_props)
    
    






# HTTP Endpoints for Regular work
# -------------------------------
# -------------------------------
# -------------------------------
# -------------------------------
@app.route(route="Holdings/{userId}", auth_level=func.AuthLevel.ANONYMOUS)
def Holdings(req: func.HttpRequest,  context: func.Context) -> func.HttpResponse:
    telemetry.info('Python HTTP trigger function processed a request.')
    
    operation_id = FunctionUtils.get_operation_id(context)
    
    tel_props = {
        Constants.operation_id: operation_id,
        Constants.SERVICE: Constants.holdings_service,
        Constants.REQUEST_METHOD: req.method
    }
    
    telemetry.info('Processing request to fetch holdings.', tel_props)
    
    user_id = req.route_params.get(Constants.REQUEST_PARAM_USER_ID)
    
    telemetry.info(f"User ID: {user_id}", tel_props)
    
    if not user_id:
        telemetry.error("Missing userId parameter", tel_props)
        return func.HttpResponse("Missing userId parameter", status_code=400)

    if req.method == Constants.HTTP_GET:
        holdings = holdings_repo.fetch_user_holdings(user_id, telemetry, tel_props)
        if holdings is not None:
            telemetry.info("Holdings found", tel_props)
            return func.HttpResponse(json.dumps(holdings), mimetype="application/json")
        else:
            telemetry.info("No holdings found", tel_props)
            return func.HttpResponse("No holdings found", status_code=404)
    
    elif req.method == Constants.HTTP_POST:
        file = req.files.get('file')
        if file:
            stream = io.StringIO(file.read().decode("UTF8"), newline=None)
            csv_reader = csv.DictReader(stream)
            holdings_data = []
            for row in csv_reader:
                holdings_data.append({
                    "Instrument": row['Instrument'],
                    "Qty": int(row['Qty.']),
                    "AvgCost": float(row['Avg. cost']),
                    "LTP": float(row['LTP']),
                    "CurVal": float(row['Cur. val']),
                    "P&L": float(row['P&L']),
                    "NetChg": float(row['Net chg.']),
                    "DayChg": float(row['Day chg.'])
                })
            holdings = holdings_repo.create_or_update_user_holdings(user_id, holdings_data, telemetry, tel_props)

            if holdings is not None:
                holdings = holdings['holdings']
                telemetry.info("Holdings created/updated", tel_props)
                return func.HttpResponse(json.dumps(holdings), mimetype="application/json")
            else:
                telemetry.error("An error occurred while creating/updating holdings", tel_props)
                return func.HttpResponse("No holdings found", status_code=404)
        else:
            telemetry.error("No file uploaded", tel_props)
            return func.HttpResponse("No file uploaded", status_code=400)
    
    else:
        telemetry.error("Method not supported", tel_props)
        return func.HttpResponse(f"Method not supported: {req.method}", status_code=405)
    
    


application_json = "application/json"
@app.route(route="alerts/{userId}", auth_level=func.AuthLevel.ANONYMOUS)
def Alerts(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
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

@app.route(route="PlotTrendLine", auth_level=func.AuthLevel.ANONYMOUS)
def PlotTrendLine(req: func.HttpRequest) -> func.HttpResponse:
    telemetry.info('Python HTTP trigger function processed a request.')

    date1 = req.params.get('date1')
    date2 = req.params.get('date2')
    ticker = req.params.get('ticker')
    chart_type = req.params.get('chart_type')
    point = req.params.get('point')

    telemetry.info(f'Received parameters: date1={date1}, date2={date2}, ticker={ticker}, chart_type={chart_type}, point={point}')

    if not point:
        point = 'Close'
    if not ticker:
        ticker = 'AAPL'

    try:
        html_string = generate_chart(date1, date2, ticker, chart_type, point)
        return func.HttpResponse(body=html_string, mimetype='text/html')
    except Exception as e:
        telemetry.error(f'An error occurred: {str(e)}.')
        return func.HttpResponse("An error occurred", status_code=500)

@app.route(route="Users", auth_level=func.AuthLevel.ANONYMOUS)
def Users(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    telemetry.info('Python HTTP trigger function processed a request.')

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
            user = User(id=user_id, user_id= user_id,email= email,name= name)
            user_repository.store_user(user, telemetry, tel_props)
            telemetry.info('User stored successfully.', tel_props)
            return func.HttpResponse("User stored successfully.", status_code=200)
        else:
            telemetry.exception('Invalid request body.', tel_props)
            return func.HttpResponse("Invalid request body.", status_code=400)
    else:
        telemetry.exception('Invalid request method.', tel_props)
        return func.HttpResponse("Invalid request method.", status_code=400)

    
@app.route( route="TickerListService", auth_level=func.AuthLevel.ANONYMOUS)
def TickerListService(req: func.HttpRequest,  context: func.Context) -> func.HttpResponse:
    telemetry.info('Python HTTP trigger function processed a request.')

    operation_id = FunctionUtils.get_operation_id(context)
    
    tel_props = {
        Constants.operation_id: operation_id,
        Constants.SERVICE: Constants.fetch_stock_info_service
    }
    
    telemetry.info('Processing request to fetch stock info.', tel_props)
    
    # Initialize RedisCacheService
    redis_cache = RedisCacheService()

    cache_key = "ticker_list"
    cached_data = redis_cache.get_value(cache_key)

    # Check if data is already in cache
    if cached_data:
        telemetry.info("Data found in cache.", tel_props)
        return func.HttpResponse(body=cached_data, mimetype='application/json')

    # If not in cache, read from Excel
    telemetry.info("Data not found in cache. Reading from Excel file.", tel_props)
    excel_path = os.getcwd() + '/Assets/TickerList.xlsx'

    try:
        df = pd.read_excel(excel_path, sheet_name='Sheet1')
        stock_info = df[['Symbol_NS', 'Company Name']].to_dict('records')
        cleaned_data = [{k: (v if pd.notna(v) else None) for k, v in record.items()} for record in stock_info]
        json_data = json.dumps(cleaned_data)

        # Save the fetched data to Redis cache
        redis_cache.set_value(cache_key, json_data)
        tel_props.update({Constants.RESPONSE_BODY: json_data, Constants.CACHE_KEY: cache_key})
        
        telemetry.info("Data saved to cache.", tel_props)
        return func.HttpResponse(body=json_data, mimetype='application/json')

    except Exception as e:
        telemetry.exception(f"An error occurred: {str(e)}", tel_props)
        return func.HttpResponse(f"An error occurred while reading the Excel file: {str(e)}", status_code=500)
    
    
    
    
    
    
# Timer Trigger Regular Automation
# -------------------------------
# -------------------------------
# -------------------------------
# -------------------------------
number_of_days = int(os.environ[Constants.number_of_days_to_fetch_participation_data])

@app.timer_trigger(schedule="0 */30 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def FetchAndStoreParticipantsData(myTimer: func.TimerRequest, context: func.Context) -> None:
    
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()


    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.fetch_store_participants_data_service,
        Constants.operation_id : operation_id,
        number_of_days : number_of_days
    }
    
    if myTimer.past_due:
        telemetry.info('The timer is past due!', tel_props)
    
    telemetry.info(f'Python timer trigger function FetchStoreParticipantsData started at {utc_timestamp}', tel_props)    
    
    fetch_store_data_for_n_days(number_of_days, tel_props)
    
    utc_timestamp = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).isoformat()
    
    telemetry.info(f'Python timer trigger function FetchStoreParticipantsData ran at {utc_timestamp} Completed', tel_props)
    

@app.timer_trigger(schedule="0 */30 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def FetchAndStoreHistoryData(myTimer: func.TimerRequest,  context: func.Context) -> None:
    
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.fetch_store_history_data_service,
        Constants.operation_id : operation_id,
    }
    
    
    telemetry.info(f'Python timer trigger function started at {utc_timestamp}', tel_props)
    
    if myTimer.past_due:
        telemetry.info('The timer is past due!', tel_props)

    fetch_store_history_data_runner(tel_props)
    
    utc_timestamp = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).isoformat()
    telemetry.info(f'Python timer trigger function FetchStoreHidstoryData completed at {utc_timestamp}', tel_props)
    
    
@app.timer_trigger(schedule="0 */30 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def TimerTriggerForAccessToken(myTimer: func.TimerRequest,  context: func.Context) -> None:
    
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.access_token_generator_service,
        Constants.operation_id : operation_id,
    }
    
    telemetry.event(f'Python timer trigger function ran at {utc_timestamp}', tel_props)

    if myTimer.past_due:
        telemetry.info('The timer is past due!', tel_props)
    
    access_token_generator_runner(tel_props)
