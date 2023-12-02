import logging
import io
import json
import csv
from SharedCode.Repository.CosmosDB.holdings_repository import HoldingsRepository
from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils

import azure.functions as func

kv_service = KeyVaultService()
database_id = kv_service.get_secret(Constants.DATABASE_ID)
holding_container_name = kv_service.get_secret(Constants.HOLDINGS_CONTAINER_NAME)
cosmos_db_service = CosmosDbService(database_id)
holdings_repo = HoldingsRepository(cosmos_db_service, holding_container_name)

telemetry = LoggerService()

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
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
