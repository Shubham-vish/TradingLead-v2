from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Utils.constants import Constants
from typing import List, Dict, Any
from dacite import from_dict
from dataclasses import asdict
from SharedCode.Models.Strategy.strategy import Strategy, StrategyUser
from SharedCode.Models.Strategy.signal_message import SignalMessage

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

    def update_strategy_executed_for_user(self, signal_message: SignalMessage, telemetry:LoggerService, tel_props: Dict[str, Any]):
        tel_props = tel_props.copy()
        tel_props.update({"action": "update_strategy_executed_for_user"})
        exception = None
        for attempt in range(3):
            try:
                strategy = self.get_strategy(signal_message.strategy_name, telemetry, tel_props)
                
                if strategy is None:
                    telemetry.exception(f"Cannot update strategy_executed_for_user. Strategy {signal_message} not found.", tel_props)
                    return
                
                other_strategy_users = [user for user in strategy.strategy_users 
                                        if (user.user_id != signal_message.user_id 
                                            or user.ticker != signal_message.ticker)]
                
                cur_strategy_user = next((strategy_user for strategy_user in strategy.strategy_users if strategy_user.ticker == signal_message.ticker and strategy_user.user_id ==  signal_message.user_id), None)
                
                cur_strategy_user.curr_quantity = signal_message.curr_quantity
                cur_strategy_user.quantity = signal_message.quantity
                
                other_strategy_users.append(cur_strategy_user)

                strategy.strategy_users = other_strategy_users
                
                updated_strategy = asdict(strategy)

                self.container.upsert_item(updated_strategy)

                telemetry.info(f"Updated strategy_executed_for_user for user {signal_message.user_id} in strategy {signal_message}.", tel_props)
                return
            except Exception as e:
                telemetry.exception_retriable(f"Attempt: {attempt} Error occurred while updating strategy_executed_for_user for user {signal_message.user_id} in strategy {signal_message}. Error: {str(e)}", tel_props)
                exception = e
        
        telemetry.exception(f"Error occurred while updating strategy_executed_for_user for user {signal_message.user_id} in strategy {signal_message}, exception:{exception}.", tel_props)
        raise exception