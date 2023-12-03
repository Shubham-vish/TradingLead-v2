import pandas as pd
import json
import os
import azure.functions as func
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Repository.Cache.redis_cache_service import RedisCacheService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils


telemetry = LoggerService()

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:

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
    excel_path = os.getcwd() + '/TickerListService/TickerList.xlsx'

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
