from azure.cosmos import PartitionKey
from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Models.Order.user_stoplosses import UserStoplosses, Stoploss, Constants as UserStoplossesConstants
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Utils.constants import Constants
from typing import List, Dict, Any
from dacite import from_dict
from dataclasses import asdict

class StoplossesRepository:
    def __init__(self):
        kv_service = KeyVaultService()
        database_id = kv_service.get_secret(Constants.DATABASE_ID)
        stop_loss_container_name = kv_service.get_secret(Constants.STOPLOSS_CONTAINER_NAME)
        cosmos_db_service = CosmosDbService(database_id)
        self.container = cosmos_db_service.get_container(stop_loss_container_name)

    def get_all_stoplosses(self, telemetry:LoggerService, tel_props) -> List[UserStoplosses]:
        tel_props = tel_props.copy()
        
        query = "SELECT * FROM c"
        
        try:
            result = self.container.query_items(query, enable_cross_partition_query=True)
            tel_props.update({Constants.COSMOS_QUERY: query, "action": "get_all_stoplosses"})
            result_list = list(result)
            if len(result_list) == 0:
                telemetry.info("No StopLosses found.", tel_props)
                return []
            else:
                telemetry.info("StopLosses found.", tel_props)
                return [from_dict(data_class=UserStoplosses, data=user_stoploss) for user_stoploss in result_list]
        except Exception as e:
            telemetry.exception(f"Error occurred while fetching all StopLosses : {str(e)}", tel_props)
            raise e
    
    def create_user_stoplosses(self, user_stoplosses:UserStoplosses, telemetry:LoggerService, tel_props):
        tel_props = tel_props.copy()
        tel_props.update({Constants.USER_ID: user_stoplosses.user_id, "action": "create_user_stoplosses"})
        
        try:
            telemetry.info(f"Creating user_stoplosses: {user_stoplosses}", tel_props)
            self.container.create_item(asdict(user_stoplosses))
            telemetry.info(f"User_stoplosses created: {user_stoplosses}", tel_props)
        except Exception as e:
            telemetry.exception(f"Error occurred while creating user_stoplosses: {str(e)}", tel_props)
            raise e

    def get_user_stoplosses(self, user_id:str, telemetry:LoggerService, tel_props)->UserStoplosses:
        tel_props = tel_props.copy()
        query = f"SELECT * FROM c WHERE c.user_id = '{user_id}'"
        tel_props.update({Constants.COSMOS_QUERY: query, "action": "get_user_stoplosses"})
        try:
            result = self.container.query_items(query, partition_key=user_id)
            result_list = list(result)
            if len(result_list) == 0:
                telemetry.info(f"StopLosses for the given user {user_id} not found.", tel_props)
                return None
            else:
                telemetry.info(f"StopLosses for the given user {user_id} found.", tel_props)
                return from_dict(data_class=UserStoplosses, data=result_list[0])
        except Exception as e:
            telemetry.exception(f"Error occurred while fetching user_stoplosses for user: {user_id} error : {str(e)}", tel_props)
            raise e

    def update_user_stoplosses(self, user_stoplosses:UserStoplosses, telemetry:LoggerService, tel_props):
        tel_props = tel_props.copy()
        tel_props.update({Constants.USER_ID: user_stoplosses.user_id, "action": "update_user_stoplosses"})
        
        try:
            telemetry.info(f"Updating user_stoplosses: {user_stoplosses}", tel_props)
            self.container.upsert_item(asdict(user_stoplosses))
            telemetry.info(f"User_stoplosses updated: {user_stoplosses}", tel_props)
        except Exception as e:
            telemetry.exception(f"Error occurred while updating user_stoplosses for user {user_stoplosses.user_id} error: {str(e)}", tel_props)
            raise e

    def delete_user_stoploss(self, user_id:str, stoploss_id:str, telemetry:LoggerService, tel_props):
        user_stoplosses = self.get_user_stoplosses(user_id, telemetry, tel_props)
        
        tel_props.update({Constants.USER_ID: user_id, Constants.STOPLOSS_ID: stoploss_id, "action": "delete_user_stoploss"})
        if user_stoplosses:
            stop_losses = user_stoplosses.stop_losses
            new_stop_losses = [stoploss for stoploss in stop_losses if stoploss.id != stoploss_id]

            if len(stop_losses) == len(new_stop_losses):
                telemetry.info(f"StopLoss for the given {stoploss_id} not found.", tel_props)
                return False
            else:
                telemetry.info(f"Stoploss for the given {stoploss_id} found. Updating the entry.", tel_props)
                user_stoplosses.stop_losses = new_stop_losses
                if len(new_stop_losses) == 0:
                    telemetry.info(f"Stoplosses for the given user {user_id} are empty. Deleting the entry.", tel_props)
                    self.container.delete_item(user_id, partition_key= user_id)
                else:
                    self.update_user_stoplosses(user_stoplosses, telemetry, tel_props)
                return True
        else:
            telemetry.info(f"StopLoss for the given user {user_id} not found.", tel_props)
            return False
            

    def store_user_stoplosses(self, user_id:str, stop_loss:Stoploss, telemetry: LoggerService, tel_props):
        tel_props = tel_props.copy()
        tel_props.update({Constants.USER_ID: user_id, "action": "store_user_stoplosses"})
        user_stoplosses = self.get_user_stoplosses(user_id, telemetry, tel_props)
        if user_stoplosses:
            telemetry.info(f"User {user_id} already has stoplosses. Updating stoplosses.", tel_props)
            user_stoplosses.add_stoploss(stop_loss)
            self.update_user_stoplosses(user_stoplosses, telemetry, tel_props)            
        else:
            telemetry.info(f"User {user_id} does not have any stoplosses. Creating stoplosses.", tel_props)
            user_stoplosses = UserStoplosses(user_id, user_id, [stop_loss])
            self.create_user_stoplosses(user_stoplosses, telemetry, tel_props)

