import logging
import pandas as pd
import json
import os

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request to fetch stock info from Excel file.')
    logging.info(f"Current working directory: {os.getcwd()}")

    # The Excel file is in the same folder as __init__.py
    excel_path = os.getcwd() + '/FetchStockInfo/TickerList.xlsx'
    
    # Read the Excel file
    try:
        df = pd.read_excel(excel_path, sheet_name='Sheet1')
    except Exception as e:
        return func.HttpResponse(f"An error occurred while reading the Excel file: {str(e)}", status_code=500)
    
    # Fetch 'Symbol_NS' and 'Company Name' columns
    stock_info = df[['Symbol_NS', 'Company Name']].to_dict('records')

    # Clean the data: Convert NaN values to None
    cleaned_data = [{k: (v if pd.notna(v) else None) for k, v in record.items()} for record in stock_info]

    # Convert the list of dictionaries to JSON and return it
    return func.HttpResponse(body=json.dumps(cleaned_data), mimetype='application/json')
