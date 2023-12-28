import datetime
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.tikers import Tickers
from SharedCode.Repository.Fyers.fyers_service import FyersService
import pandas as pd
from SharedCode.Repository.BlobService.blob_service import BlobService
from SharedCode.Utils.constants import Constants

kv_service = KeyVaultService()
blob_service = BlobService()
telemetry = LoggerService()


def fetch_store_history_data_runner(tel_props):
    fyers_details = kv_service.get_fyers_user(0)
    fyers_service = FyersService(fyers_details)

    tickers = Tickers.nifty_50_stocks
    
    tel_props.update({"action": "fetch_store_history_data_runner"})
    telemetry.info("fetch_store_history_data_runner started", tel_props)
    
    for ticker in tickers:
        try:
            df = pd.DataFrame()
            sd = datetime.date(2017, 7, 3)
            enddate = datetime.datetime.now().date()
            telemetry.info(f"fetching data for {ticker} from {sd} to {enddate}", tel_props)
            fyers_service.fetch_deep_history(ticker, sd, enddate, resolution="1", tel_props=tel_props)
            ticker = ticker.replace(":", "_")
            blob_name = f"{Constants.DIR_NIFTY_50}/{ticker}.csv"
            result = blob_service.create_blob(df, Constants.STOCK_HISTORY_CONTAINER, blob_name)
            telemetry.info(f"fetching data for {ticker} from {sd} to {enddate} completed, {result}", tel_props)
        except Exception as e:
            telemetry.exception(f"fetching data for {ticker} from {sd} to {enddate} failed with exception: {e}", tel_props)