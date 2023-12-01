import uuid
import logging
from azure.cosmos import exceptions

class HoldingsRepository:
    def __init__(self, cosmos_service, container_name):
        self.container = cosmos_service.get_container(container_name)

    def fetch_user_holdings(self, user_id):
        logging.info(f"Fetching holdings for user ID: {user_id}")
        query = f"SELECT * FROM c WHERE c.userId = @userId"
        parameters = [{'name': '@userId', 'value': user_id}]
        try:
            items = list(self.container.query_items(
                query=query, 
                parameters=parameters, 
                enable_cross_partition_query=True))
            return items[0]['holdings'] if items else None
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"An error occurred while fetching holdings: {e}")
            return None

    def create_or_update_user_holdings(self, user_id, holdings_data):
        logging.info(f"Creating or updating holdings for user ID: {user_id}")
        query = f"SELECT * FROM c WHERE c.userId = @userId"
        parameters = [{'name': '@userId', 'value': user_id}]
        try:
            items = list(self.container.query_items(
                query=query, 
                parameters=parameters, 
                enable_cross_partition_query=True))

            if not items:
                # Create new record
                new_entry = {
                    "id": str(uuid.uuid4()),
                    "userId": user_id,
                    "holdings": holdings_data
                }
                self.container.create_item(new_entry)
                return new_entry
            else:
                # Update existing record
                existing_entry = items[0]
                existing_entry['holdings'] = holdings_data
                self.container.replace_item(item=existing_entry['id'], body=existing_entry)
                return existing_entry
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"An error occurred while creating/updating holdings: {e}")
            return None

    def delete_user_holdings(self, user_id):
        logging.info(f"Deleting holdings for user ID: {user_id}")
        query = f"SELECT * FROM c WHERE c.userId = @userId"
        parameters = [{'name': '@userId', 'value': user_id}]
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
            logging.error(f"An error occurred while deleting holdings: {e}")
            return False
