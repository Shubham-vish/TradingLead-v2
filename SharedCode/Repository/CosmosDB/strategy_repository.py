from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Utils.constants import Constants
from typing import List, Dict, Any
from dacite import from_dict
from dataclasses import asdict
from SharedCode.Models.Strategy.strategy import Strategy, StrategyUser

class StrategyRepository:
    def __init__(self):
        kv_service = KeyVaultService()
        database_id = kv_service.get_secret(Constants.DATABASE_ID)
        strategy_container_name = kv_service.get_secret(Constants.STRATEGY_CONTAINER_NAME)
        cosmos_db_service = CosmosDbService(database_id)
        self.container = cosmos_db_service.get_container(strategy_container_name)

    def get_strategy(self, strategy_name:str, telemetry:LoggerService, tel_props)->Strategy:
        tel_props = tel_props.copy()
        query = f"SELECT * FROM c WHERE c.strategy_name = '{strategy_name}'"
        tel_props.update({Constants.COSMOS_QUERY: query, "action": "get_strategy"})
        try:
            result = self.container.query_items(query, partition_key=strategy_name)
            result_list = list(result)
            if len(result_list) == 0:
                telemetry.info(f"Strategy for the given strategy_name {strategy_name} not found.", tel_props)
                return None
            else:
                telemetry.info(f"Strategy for the given strategy_name {strategy_name} found.", tel_props)
                strategy = from_dict(data_class=Strategy, data=result_list[0])
                return strategy
        except Exception as e:
            telemetry.exception(f"Error occurred while fetching strategy for strategy_name: {strategy_name} error : {str(e)}", tel_props)
            raise e
    
    
    def add_user_to_strategy(self, strategy_name: str, strategy_user: StrategyUser, telemetry: LoggerService, tel_props: Dict[str, Any]):
        tel_props = tel_props.copy()
        tel_props.update({"action": "add_user_to_strategy"})
        try:
            strategy = self.get_strategy(strategy_name, telemetry, tel_props)
            
            if strategy is None:
                telemetry.info(f"Cannot add user to strategy. Strategy {strategy_name} not found.", tel_props)
                return

            
            # Remove existing strategy user with the same id
            strategy.strategy_users = [user for user in strategy.strategy_users 
                                       if (user.user_id != strategy_user.user_id 
                                           or user.ticker != strategy_user.ticker)]
            
            strategy.strategy_users.append(strategy_user)

            updated_strategy = asdict(strategy)

            self.container.upsert_item(updated_strategy)

            telemetry.info(f"User added to strategy {strategy_name}.", tel_props)
        except Exception as e:
            telemetry.exception(f"Error occurred while adding user to strategy {strategy_name}. Error: {str(e)}", tel_props)
            raise e
