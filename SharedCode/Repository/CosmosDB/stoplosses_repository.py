from azure.cosmos import PartitionKey
from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Models.user_stoplosses import UserStoplosses, Stoploss, Constants as UserStoplossesConstants
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Utils.constants import Constants
from typing import List, Dict, Any

class StoplossesRepository:
    def __init__(self):
        kv_service = KeyVaultService()
        database_id = kv_service.get_secret(Constants.DATABASE_ID)
        stop_loss_container_name = kv_service.get_secret(Constants.STOPLOSS_CONTAINER_NAME)
        cosmos_db_service = CosmosDbService(database_id)
        self.container = cosmos_db_service.get_container(stop_loss_container_name)

    def get_all_stoplosses(self, telemetry:LoggerService, tel_props) -> List[UserStoplosses]:
        query = "SELECT * FROM c"
        result = self.container.query_items(query, enable_cross_partition_query=True)
        tel_props.update({Constants.COSMOS_QUERY: query, "action": "get_all_stoplosses"})
        result_list = list(result)
        if len(result_list) == 0:
            telemetry.info("No StopLosses found.", tel_props)
            return None
        else:
            telemetry.info("StopLosses found.", tel_props)
            user_stoplosses_list = []
            for item in result_list:
                try:
                    user_stoplosses = UserStoplosses.from_dict(item)
                    user_stoplosses_list.append(user_stoplosses)
                except Exception as e:
                    telemetry.error(f"Error occurred while processing user stoplosses doc: {item}, error: {str(e)}", tel_props)
            return user_stoplosses_list
    
    def create_user_stoplosses(self, stoploss):
        self.container.create_item(stoploss)

    def get_user_stoplosses(self, user_id:str, telemetry:LoggerService, tel_props):
        query = f"SELECT * FROM c WHERE c.UserId = '{user_id}'"
        result = self.container.query_items(query, enable_cross_partition_query=True)
        tel_props.update({Constants.COSMOS_QUERY: query, "action": "get_user_stoplosses"})
        result_list = list(result)
        if len(result_list) == 0:
            telemetry.info(f"StopLosses for the given user {user_id} not found.", tel_props)
            return None
        else:
            telemetry.info(f"StopLosses for the given user {user_id} found.", tel_props)
            return result_list[0]

    def update_user_stoplosses(self, user_stoplosses):
        self.container.upsert_item(user_stoplosses)

    def delete_user_stoploss(self, user_id:str, stoploss_id:str, telemetry:LoggerService, tel_props):
        user_stoplosses_dict = self.get_user_stoplosses(user_id, telemetry, tel_props)
        
        tel_props.update({Constants.USER_ID: user_id, Constants.STOPLOSS_ID: stoploss_id, "action": "delete_user_stoploss"})
        if user_stoplosses_dict:
            user_stoplosses = UserStoplosses.from_dict(user_stoplosses_dict)
            stop_losses = user_stoplosses.stop_losses
            new_stop_losses = [stoploss for stoploss in stop_losses if stoploss.id != stoploss_id]

            if len(stop_losses) == len(new_stop_losses):
                telemetry.info(f"StopLoss for the given {stoploss_id} not found.", tel_props)
                return False
            else:
                telemetry.info(f"Stoploss for the given {stoploss_id} found. Updating the entry.", tel_props)
                user_stoplosses.stop_losses = new_stop_losses
                self.update_user_stoplosses(user_stoplosses.to_dict())
                return True
        else:
            telemetry.info(f"StopLoss for the given user {user_id} not found.", tel_props)
            return False
            

    def store_user_stoplosses(self, user_id:str, stop_loss:Stoploss, telemetry: LoggerService, tel_props):
        user_stoplosses_dict = self.get_user_stoplosses(user_id, telemetry, tel_props)
        if user_stoplosses_dict:
            # Existing stoplosses found for the user
            telemetry.info(f"User {user_id} already has stoplosses. Updating stoplosses.", tel_props)
            
            stop_losses = user_stoplosses_dict[UserStoplossesConstants.stoplosses]
            stop_loss_id = stop_loss.id
            stop_loss_exists = False

            for i, sl in enumerate(stop_losses):
                if sl["id"] == stop_loss_id:
                    stop_losses[i] = stop_loss.to_dict()
                    stop_loss_exists = True
                    break

            if not stop_loss_exists:
                stop_losses.append(stop_loss.to_dict())

            self.update_user_stoplosses(user_stoplosses_dict)            
        else:
        # No existing stoplosses found for the user
            telemetry.info(f"User {user_id} does not have any stoplosses. Creating stoplosses.", tel_props)
            user_stoplosses = UserStoplosses(user_id, user_id, [stop_loss])
            doc_db_object = user_stoplosses.to_dict()
            self.create_user_stoplosses(doc_db_object)

