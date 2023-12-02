import uuid
import json
from azure.cosmos import exceptions
from SharedCode.Utils.constants import Constants

class HoldingsRepository:
    def __init__(self, cosmos_service, container_name):
        self.container = cosmos_service.get_container(container_name)

    def fetch_user_holdings(self, user_id, telemetry, tel_props):
        query = f"SELECT * FROM c WHERE c.userId = @userId"
        parameters = [{'name': '@userId', 'value': user_id}]
        
        tel_props.update({
            Constants.COSMOS_QUERY: query,
            Constants.COSMOS_PARAMS: json.dumps(parameters)
        })
        
        telemetry.info(f"Fetching holdings from CosmosDB for userID: {user_id}", tel_props)
        
        try:
            items = list(self.container.query_items(
                query=query, 
                parameters=parameters, 
                enable_cross_partition_query=True))
            return items[0]['holdings'] if items else None
        except exceptions.CosmosHttpResponseError as e:
            telemetry.exception(f"An error occurred while fetching holdings: {e}")
            raise e

    def create_or_update_user_holdings(self, user_id, holdings_data, telemetry, tel_props):
        query = f"SELECT * FROM c WHERE c.userId = @userId"
        parameters = [{'name': '@userId', 'value': user_id}]
        
        tel_props.update({
            Constants.COSMOS_QUERY: query,
            Constants.COSMOS_PARAMS: json.dumps(parameters)
        })
        
        telemetry.info(f"Creating/Updating holdings in CosmosDB for userID: {user_id}", tel_props)
        
        try:
            items = list(self.container.query_items(
                query=query, 
                parameters=parameters, 
                enable_cross_partition_query=True))

            if not items:
                # Create new record
                telemetry.info(f"Creating new Cosmos record for userID: {user_id}", tel_props)
                new_entry = {
                    "id": str(uuid.uuid4()),
                    "userId": user_id,
                    "holdings": holdings_data
                }
                self.container.create_item(new_entry)
                return new_entry
            else:
                # Update existing record
                telemetry.info(f"Updating existing record for userID: {user_id}", tel_props)
                existing_entry = items[0]
                existing_entry['holdings'] = holdings_data
                self.container.replace_item(existing_entry, existing_entry)
                return existing_entry
        except exceptions.CosmosHttpResponseError as e:
            telemetry.exception(f"An error occurred while creating/updating holdings: {e}", tel_props)
            raise e

    def delete_user_holdings(self, user_id, telemetry, tel_props):
        query = f"SELECT * FROM c WHERE c.userId = @userId"
        parameters = [{'name': '@userId', 'value': user_id}]
        
        tel_props.update({
            Constants.COSMOS_QUERY: query,
            Constants.COSMOS_PARAMS: json.dumps(parameters)
        })
        
        telemetry.info(f"Deleting holdings for user ID: {user_id}", tel_props)
        try:
            items = list(self.container.query_items(
                query=query, 
                parameters=parameters, 
                enable_cross_partition_query=True))
            if items:
                self.container.delete_item(item=items[0], partition_key=user_id)
                return True
            return False
        except exceptions.CosmosHttpResponseError as e:
            telemetry.exception(f"An error occurred while deleting holdings: {e}", tel_props)
            raise e
