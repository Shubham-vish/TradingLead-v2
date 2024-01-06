from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Repository.ServiceBus.servicebus_service import ServiceBusService
from dataclasses import asdict
from SharedCode.Repository.CosmosDB.strategy_repository import StrategyRepository
import json
import concurrent.futures
from SharedCode.Repository.Fyers.fyers_service import FyersService
from SharedCode.Models.Strategy.strategy import Strategy, StrategyUser
from SharedCode.Strategies.ml import KernelRegressionStrategy
import datetime
from SharedCode.Models.Strategy.signal_message import SignalMessage

kv_service = KeyVaultService()
telemetry = LoggerService()
sb_service = ServiceBusService()
strategy_repo = StrategyRepository()


fyers_details = kv_service.get_fyers_user(0)
fyers_service = FyersService(fyers_details)
kernel_strategy = KernelRegressionStrategy()

strategy_name = "KernelRegressionStrategy"

signal_topic_name = "signal-topic"


def send_signal_message(strategy_user:StrategyUser, buy_signal:bool, ltp:float,  tel_props):
    tel_props = tel_props.copy()
    telemetry.info(f"Sending signal message for user, ticker: {strategy_user.user_id}, {strategy_user.ticker} with signal: {buy_signal}", tel_props)
    signal_message = SignalMessage.from_strategy_user(strategy_user, strategy_name, buy_signal, ltp)
    sb_service.send_to_topic(json.dumps(asdict(signal_message)), signal_topic_name)
    
    tel_props.update({"signal_message": asdict(signal_message)})
    telemetry.info(f"Signal message sent for user, ticker: {strategy_user.user_id}, {strategy_user.ticker} with signal: {buy_signal}, ltp: {ltp}", tel_props)

def process_strategy_user(strategy_user:StrategyUser, strategy:Strategy, tel_props):
    
    tel_props = tel_props.copy()
    tel_props.update({"action": "process_strategy_user", "strategy_user": json.dumps(asdict(strategy_user))})
    
    time_delta_in_days = strategy.strategy_details["time_delta_in_days"]
    resolution = strategy.strategy_details["resolution"]
    # End date need to be tested if it is in IST to UTC
    end_date = datetime.datetime.now().date()
    start_date = datetime.datetime.now().date() - datetime.timedelta(days=time_delta_in_days)
    
    df = fyers_service.history(strategy_user.ticker, start_date, end_date, resolution, tel_props)
    df = df.iloc[::-1]
    
    # df = df.sort_index()  # Sort the DataFrame based on datetime index
      # Remove any duplicate rows based on datetime index
    # df.head(50)
    
    telemetry.info(f"History fetched for ticker: {strategy_user.ticker} with shape: {df.shape}, head: {df.head()}", tel_props)
    
    df = kernel_strategy.get_yhat1_with_signals(df, "close")
    df.head(10)
    # StockChart.plot_chart_with_yhat(df, strategy_user.ticker, resolution)
    
    telemetry.info(f"yhat1 calculated for ticker: {strategy_user.ticker} with shape: {df.shape}, head: {df.head(2)}", tel_props)
    
    buy_signal = df['pyhat'].notnull().iloc[0]
    
    telemetry.info(f"KernelStrategy buy_signal: {buy_signal}, for ticker: {strategy_user.ticker}", tel_props)

    ltp = df['close'].iloc[0]
    
    send_signal_message(strategy_user, buy_signal, ltp, tel_props)


def strategy_kernel_regression_runner(tel_props):
    tel_props = tel_props.copy()
    tel_props.update({"action": "strategy_kernel_regression_runner"})    
    telemetry.info(f"strategy_kernel_regression_runner started", tel_props)
    strategy = strategy_repo.get_strategy(strategy_name, telemetry, tel_props)
    
    strategy_users = strategy.strategy_users
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit each strategy user to the executor for parallel processing
        futures = [executor.submit(process_strategy_user, strategy_user, strategy, tel_props) for strategy_user in strategy_users]
        
        # Wait for all futures to complete
        concurrent.futures.wait(futures)
        
        # Get the result from each future and log it
        for future in futures:
            result = future.result()
            telemetry.info(f"Result: {result}", tel_props)
    
    
    
    
    
    
