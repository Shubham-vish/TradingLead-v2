import uuid
import json
from azure.cosmos import exceptions
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
import datetime

class ParticipantsDataCosmosRepository:
    def __init__(self, cosmos_service, container_name):
        self.container = cosmos_service.get_container(container_name)
        
    def store_data_for_day(self, date, df, telemetry, tel_props):
        # Convert DataFrame to a JSON document
        document = df.to_dict(orient='records')

        # Create a unique ID using the date
        date_str = date.strftime('%d-%m-%Y')
        date_for_id = date.strftime('%d-%m-%Y-%a')
        stored_time = FunctionUtils.get_ist_time().strftime('%d-%m-%Y-%a %H:%M:%S')
        document_id = f"participantsData_{date_for_id}"

        # Prepare the document for Cosmos DB
        cosmos_document = {
            "id": document_id,
            "date": date_str,
            "stored_time": stored_time,
            "data": document
        }

        try:
            # Store or update the document in Cosmos DB
            self.container.upsert_item(cosmos_document)
            telemetry.info(f"Stored data for {date_str}", tel_props)
        except exceptions.CosmosHttpResponseError as e:
            telemetry.error(f"Failed to store data for {date_str}: {e}", tel_props)

        telemetry.info(f"Completed storing data for {date_str}", tel_props)
        
    def delete_all_data(self, telemetry, tel_props):
        try:
            # Fetch all the items in the container
            items = self.container.query_items(
                query="SELECT * FROM c",
                enable_cross_partition_query=True
            )

            # Iterate over the items and delete each one
            for item in items:
                self.container.delete_item(item, partition_key=item['date'])
                telemetry.info(f"Deleted item with id: {item['id']}", tel_props)

            telemetry.info("All data deleted from the container", tel_props)
        except exceptions.CosmosHttpResponseError as e:
            telemetry.error(f"Failed to delete data: {e}", tel_props)


    # def fetch_user_holdings(self, user_id, telemetry, tel_props):
    #     query = f"SELECT * FROM c WHERE c.userId = @userId"
    #     parameters = [{'name': '@userId', 'value': user_id}]
        
    #     tel_props.update({
    #         Constants.COSMOS_QUERY: query,
    #         Constants.COSMOS_PARAMS: json.dumps(parameters)
    #     })
        
    #     telemetry.info(f"Fetching holdings from CosmosDB for userID: {user_id}", tel_props)
        
    #     try:
    #         items = list(self.container.query_items(
    #             query=query, 
    #             parameters=parameters, 
    #             enable_cross_partition_query=True))
    #         return items[0]['holdings'] if items else None
    #     except exceptions.CosmosHttpResponseError as e:
    #         telemetry.exception(f"An error occurred while fetching holdings: {e}")
    #         raise e

    # def create_or_update_user_holdings(self, user_id, holdings_data, telemetry, tel_props):
    #     query = f"SELECT * FROM c WHERE c.userId = @userId"
    #     parameters = [{'name': '@userId', 'value': user_id}]
        
    #     tel_props.update({
    #         Constants.COSMOS_QUERY: query,
    #         Constants.COSMOS_PARAMS: json.dumps(parameters)
    #     })
        
    #     telemetry.info(f"Creating/Updating holdings in CosmosDB for userID: {user_id}", tel_props)
        
    #     try:
    #         items = list(self.container.query_items(
    #             query=query, 
    #             parameters=parameters, 
    #             enable_cross_partition_query=True))

    #         if not items:
    #             # Create new record
    #             telemetry.info(f"Creating new Cosmos record for userID: {user_id}", tel_props)
    #             new_entry = {
    #                 "id": str(uuid.uuid4()),
    #                 "userId": user_id,
    #                 "holdings": holdings_data
    #             }
    #             self.container.create_item(new_entry)
    #             return new_entry
    #         else:
    #             # Update existing record
    #             telemetry.info(f"Updating existing record for userID: {user_id}", tel_props)
    #             existing_entry = items[0]
    #             existing_entry['holdings'] = holdings_data
    #             self.container.replace_item(existing_entry, existing_entry)
    #             return existing_entry
    #     except exceptions.CosmosHttpResponseError as e:
    #         telemetry.exception(f"An error occurred while creating/updating holdings: {e}", tel_props)
    #         raise e

    # def delete_user_holdings(self, user_id, telemetry, tel_props):
    #     query = f"SELECT * FROM c WHERE c.userId = @userId"
    #     parameters = [{'name': '@userId', 'value': user_id}]
        
    #     tel_props.update({
    #         Constants.COSMOS_QUERY: query,
    #         Constants.COSMOS_PARAMS: json.dumps(parameters)
    #     })
        
    #     telemetry.info(f"Deleting holdings for user ID: {user_id}", tel_props)
    #     try:
    #         items = list(self.container.query_items(
    #             query=query, 
    #             parameters=parameters, 
    #             enable_cross_partition_query=True))
    #         if items:
    #             self.container.delete_item(item=items[0], partition_key=user_id)
    #             return True
    #         return False
    #     except exceptions.CosmosHttpResponseError as e:
    #         telemetry.exception(f"An error occurred while deleting holdings: {e}", tel_props)
    #         raise e
