import logging
import csv
import io
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from Repository.cosmos_db_repository import create_or_update_user_holdings, fetch_user_holdings

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    user_id = req.params.get('userId')
    if not user_id:
        return func.HttpResponse("Missing userId parameter", status_code=400)

    if req.method == "GET":
        holdings = fetch_user_holdings(user_id)
        if holdings is not None:
            return func.HttpResponse(json.dumps(holdings), mimetype="application/json")
        else:
            return func.HttpResponse("No holdings found", status_code=404)
    
    elif req.method == "POST":
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
            holdings = create_or_update_user_holdings(user_id, holdings_data)

            if holdings is not None:
                return func.HttpResponse(json.dumps(holdings), mimetype="application/json")
            else:
                return func.HttpResponse("No holdings found", status_code=404)
        else:
            return func.HttpResponse("No file uploaded", status_code=400)
    
    else:
        return func.HttpResponse("Method not supported", status_code=405)
