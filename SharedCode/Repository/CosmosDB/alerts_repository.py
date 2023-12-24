import uuid
from azure.cosmos import exceptions
from SharedCode.Utils.constants import Constants
import json

class AlertsRepository:
    def __init__(self, cosmos_service, container_name):
        self.container = cosmos_service.get_container(container_name)

    def fetch_user_alerts(self, user_id, telemetry, tel_props):
        query = "SELECT * FROM c WHERE c.userId = @userId"
        parameters = [{'name': '@userId', 'value': user_id}]
        
        tel_props.update({
            Constants.COSMOS_QUERY: query,
            Constants.COSMOS_PARAMS: json.dumps(parameters)
        })
        
        telemetry.info(f"Fetching alerts for user ID: {user_id}", tel_props)

        items = list(self.container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True))
        if len(items) > 0:
            telemetry.info("Returning alerts from alertsRepo.", tel_props)
            return items[0]
        else:
            telemetry.info("No alerts found in Cosmos DB.", tel_props)
            return None
        

    def create_user_alert(self, user_id, trend_start, trend_end, ticker, stock_name, telemetry, tel_props):
        telemetry.info(f"Creating alert for user ID: {user_id}, ticker: {ticker}", tel_props)
        query = f"SELECT * FROM c WHERE c.userId = '{user_id}'"
        telemetry.info(f"Query: {query}", tel_props)
        items = list(self.container.query_items(query, enable_cross_partition_query=True))
        tel_props.update({"ItemsFetched": json.dumps(items) if items else "None"})
        telemetry.info(f"Items fetched: {len(items)}", tel_props)
        
        if len(items) == 0:
            telemetry.info("User alerts not found. Creating new entry.")
            new_entry = {
                "id": str(uuid.uuid4()),
                "userId": user_id,
                "Alerts": [
                    {
                        "trendStart": trend_start,
                        "trendEnd": trend_end,
                        "ticker": ticker,
                        "StockName": stock_name
                    }
                ]
            }
            self.container.create_item(new_entry)
            
            telemetry.info("New entry created.", tel_props)
        else:
            telemetry.info("User Alerts found. Updating existing entry.")
            existing_entry = items[0]
            self.update_user_alert(existing_entry, trend_start, trend_end, ticker, stock_name, telemetry, tel_props)


    def update_user_alert(self, existing_entry, trend_start, trend_end, ticker, stock_name, telemetry, tel_props):
        tel_props.update({"ExistingEntry": json.dumps(existing_entry)})
        telemetry.info(f"Updating alert for ticker: {ticker}", tel_props)
        existing_alerts = existing_entry.get("Alerts", [])
        existing_ticker_alert = next((alert for alert in existing_alerts if alert["ticker"] == ticker), None)

        if existing_ticker_alert:
            telemetry.info("Ticker found. Updating existing alert.", tel_props)
            existing_ticker_alert["trendStart"] = trend_start
            existing_ticker_alert["trendEnd"] = trend_end
        else:
            telemetry.info("Ticker not found. Adding new alert.", tel_props)
            existing_alerts.append({
                "trendStart": trend_start,
                "trendEnd": trend_end,
                "ticker": ticker,
                "StockName": stock_name
            })
        existing_entry["Alerts"] = existing_alerts
        self.container.replace_item(existing_entry, existing_entry)
        telemetry.info("Alert updated.")
        
    
    def delete_user_alert(self, user_id, ticker, telemetry, tel_props):
        telemetry.info(f"Deleting alert for user ID: {user_id}, ticker: {ticker}", tel_props)
        query = f"SELECT * FROM c WHERE c.userId = '{user_id}'"
        telemetry.info(f"Query: {query}", tel_props)
        items = list(self.container.query_items(query, enable_cross_partition_query=True))
        tel_props.update({"ItemsFetched": json.dumps(items) if items else "None"})

        
        telemetry.info(f"Items fetched: {len(items)}", tel_props)

        if len(items) == 0:
            telemetry.info("User Alerts not found.", tel_props)
            return

        existing_entry = items[0]
        existing_alerts = existing_entry.get("Alerts", [])
        new_alerts = [alert for alert in existing_alerts if alert["ticker"] != ticker]

        if len(new_alerts) == len(existing_alerts):
            telemetry.info("Alert for the given Ticker not found.", tel_props)
            return

        existing_entry["Alerts"] = new_alerts
        self.container.replace_item(existing_entry, existing_entry)
        telemetry.info(f"Alert for ticker {ticker} deleted.", tel_props)
