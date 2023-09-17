from azure.cosmos import CosmosClient, PartitionKey
import uuid
import logging

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


vault_url = "https://kv-tradinglead.vault.azure.net/"
credential = DefaultAzureCredential()
kvClient = SecretClient(vault_url=vault_url, credential=credential)

# Fetch secrets


# Initialize Cosmos DB client
logging.info("Initializing Cosmos DB client.")

url = kvClient.get_secret("CosmosDbUrl").value
key = kvClient.get_secret("CosmosDbKey").value

cosmos_client = CosmosClient(url, credential=key)

database = cosmos_client.get_database_client("TradingLead")
alertsContainer = database.get_container_client(kvClient.get_secret("CosmosAlertsContainer").value)


# Initialize Holdings alertsContainerd
holdings_container = database.create_container_if_not_exists(
    id=kvClient.get_secret("CosmosHoldingsContainer").value,
    partition_key=PartitionKey(path="/userId"),
)

def fetch_user_holdings(user_id):
    logging.info(f"Fetching holdings for user ID: {user_id}")
    query = f"SELECT * FROM c WHERE c.userId = '{user_id}'"
    items = list(holdings_container.query_items(query, enable_cross_partition_query=True))
    if len(items) > 0:
        return items[0]['holdings']
    else:
        return None

def create_or_update_user_holdings(user_id, holdings_data):
    logging.info(f"Creating or updating holdings for user ID: {user_id}")
    query = f"SELECT * FROM c WHERE c.userId = '{user_id}'"
    items = list(holdings_container.query_items(query, enable_cross_partition_query=True))

    updated_holdings = None

    if len(items) == 0:
        # Create new record
        new_entry = {
            "id": str(uuid.uuid4()),
            "userId": user_id,
            "holdings": holdings_data  # holdings_data is already processed
        }
        holdings_container.create_item(new_entry)
        updated_holdings = holdings_data
    else:
        # Update existing record
        existing_entry = items[0]
        existing_entry['holdings'] = holdings_data  # holdings_data is already processed
        holdings_container.replace_item(existing_entry, existing_entry)
        updated_holdings = holdings_data

    return updated_holdings


# Optionally, you can add a function to delete user holdings
def delete_user_holdings(user_id):
    logging.info(f"Deleting holdings for user ID: {user_id}")
    query = f"SELECT * FROM c WHERE c.userId = '{user_id}'"
    items = list(holdings_container.query_items(query, enable_cross_partition_query=True))
    if len(items) > 0:
        holdings_container.delete_item(items[0], partition_key=user_id)

def fetch_user_alerts(user_id):
    logging.info(f"Fetching alerts for user ID: {user_id}")
    query = f"SELECT * FROM c WHERE c.userId = '{user_id}'"
    logging.info(f"Query: {query}")
    items = list(alertsContainer.query_items(query, enable_cross_partition_query=True))
    logging.info(f"Items fetched: {len(items)}")
    if len(items) > 0:
        logging.info("Returning first item.")
        return items[0]
    else:
        logging.warning("No items found.")
        return None

def create_user_alert(user_id, trend_start, trend_end, ticker, stock_name):
    logging.info(f"Creating alert for user ID: {user_id}, ticker: {ticker}")
    query = f"SELECT * FROM c WHERE c.userId = '{user_id}'"
    logging.info(f"Query: {query}")
    items = list(alertsContainer.query_items(query, enable_cross_partition_query=True))
    logging.info(f"Items fetched: {len(items)}")
    
    if len(items) == 0:
        logging.info("User not found. Creating new entry.")
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
        alertsContainer.create_item(new_entry)
        logging.info("New entry created.")
    else:
        logging.info("User found. Updating existing entry.")
        existing_entry = items[0]
        update_user_alert(existing_entry, trend_start, trend_end, ticker, stock_name)

def update_user_alert(existing_entry, trend_start, trend_end, ticker, stock_name):
    logging.info(f"Updating alert for ticker: {ticker}")
    existing_alerts = existing_entry.get("Alerts", [])
    existing_ticker_alert = next((alert for alert in existing_alerts if alert["ticker"] == ticker), None)

    if existing_ticker_alert:
        logging.info("Ticker found. Updating existing alert.")
        existing_ticker_alert["trendStart"] = trend_start
        existing_ticker_alert["trendEnd"] = trend_end
    else:
        logging.info("Ticker not found. Adding new alert.")
        existing_alerts.append({
            "trendStart": trend_start,
            "trendEnd": trend_end,
            "ticker": ticker,
            "StockName": stock_name
        })
    existing_entry["Alerts"] = existing_alerts
    alertsContainer.replace_item(existing_entry, existing_entry)
    logging.info("Alert updated.")

def delete_user_alert(user_id, ticker):
    logging.info(f"Deleting alert for user ID: {user_id}, ticker: {ticker}")
    query = f"SELECT * FROM c WHERE c.userId = '{user_id}'"
    logging.info(f"Query: {query}")
    items = list(alertsContainer.query_items(query, enable_cross_partition_query=True))
    logging.info(f"Items fetched: {len(items)}")

    if len(items) == 0:
        logging.warning("User not found.")
        return

    existing_entry = items[0]
    existing_alerts = existing_entry.get("Alerts", [])
    new_alerts = [alert for alert in existing_alerts if alert["ticker"] != ticker]

    if len(new_alerts) == len(existing_alerts):
        logging.warning("Ticker not found.")
        return

    existing_entry["Alerts"] = new_alerts
    alertsContainer.replace_item(existing_entry, existing_entry)
    logging.info(f"Alert for ticker {ticker} deleted.")


