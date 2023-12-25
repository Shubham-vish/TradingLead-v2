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