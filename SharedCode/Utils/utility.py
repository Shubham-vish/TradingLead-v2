from datetime import datetime, timedelta
import pandas as pd
from SharedCode.Repository.Cache.redis_cache_service import RedisCacheService

class FunctionUtils:
    @staticmethod
    def get_operation_id(context):
        traceparent = context.trace_context.Traceparent
        try:
            operation_id = f"{traceparent}".split("-")[1]
        except IndexError:
            operation_id = "default_id"
        return operation_id

    @staticmethod
    def get_ist_time(time=None):
        utc_time = time if time is not None else datetime.utcnow()
        # IST is UTC + 5 hours 30 minutes
        ist_time = utc_time + timedelta(hours=5, minutes=30)
        return ist_time

    @staticmethod
    def get_key_for_user_access_token(username):
        redis_key = f"{username}-token"
        return redis_key
    
    @staticmethod
    def get_key_for_yfinance(ticker, period):
        redis_key = f"{ticker}-{period}-yfinance4"
        return redis_key

    @staticmethod
    def get_storage_ticker(ticker):
        return ticker.replace(":", "_")
    
    @staticmethod
    def set_symbol_ns_for_fyers_ticker(ticker, product_type, symbol_ns):
        redis_cache = RedisCacheService()
        redis_cache_key = f"{ticker}:{product_type}:symbol_ns"
        redis_cache.set_value(redis_cache_key, symbol_ns)
        return symbol_ns
    
    @staticmethod
    def get_symbol_ns_from_fyers_ticker(ticker, product_type):
        return ticker
    
    @staticmethod
    def set_trade_ticker_for_fyers_ticker(ticker, product_type, trade_ticker):
        redis_cache = RedisCacheService()
        redis_cache_key = f"{ticker}:{product_type}:trade_ticker"
        redis_cache.set_value(redis_cache_key, trade_ticker)
        return trade_ticker
    
    @staticmethod
    def get_trade_ticker_from_fyers_ticker(ticker, product_type):
        redis_cache = RedisCacheService()
        redis_cache_key = f"{ticker}:{product_type}:trade_ticker"
        redis_cache_value = redis_cache.get_decoded_value(redis_cache_key)
        return redis_cache_value    
    

    @staticmethod
    def filter_last_n_days(df: pd.DataFrame, n=20) -> pd.DataFrame:
        """
        Filters the DataFrame to include only the last N days of data.

        :param df: Pandas DataFrame with a DateTimeIndex.
        :param n: Number of days to filter on.
        :return: Filtered DataFrame.
        """
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("DataFrame index must be a DatetimeIndex.")

        return df[df.index >= df.index.max() - pd.Timedelta(days=n)]

    @staticmethod
    def resample_to_timeframe(df:pd.DataFrame, frequency="30T") -> pd.DataFrame:
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("DataFrame index must be a DatetimeIndex.")

        # Make a copy of the DataFrame to avoid modifying the original
        resampled_df = df.copy()

        # Define aggregation rules for OHLCV data
        ohlc_dict = {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }

        # Adjust the index for resampling if the frequency is intraday
        if "T" in frequency or "H" in frequency:
            # Adjust to start at 9:00 AM, making 9:15 to 9:00 to perform correct resampling
            resampled_df.index = resampled_df.index - pd.Timedelta(minutes=15)
            resampled_df = resampled_df.resample(frequency, origin="start_day").agg(
                ohlc_dict
            )
            # Adjust back to start at 9:15 AM
            resampled_df.index = resampled_df.index + pd.Timedelta(minutes=15)
        else:
            # For daily or higher frequencies, no need to adjust the index
            resampled_df = resampled_df.resample(frequency).agg(ohlc_dict)

        # Drop NA values that may have been created by resampling
        resampled_df.dropna(inplace=True)

        return resampled_df


    # utils.are_dataframes_identical(
    #     utils.resample_to_timeframe(fdf, "60T"),
    #     utils.resample_to_timeframe(fdf, "1H"),
    # )
    @staticmethod
    def are_dataframes_identical(df1: pd.DataFrame, df2: pd.DataFrame):
        """
        Compares two DataFrames to determine if they are identical.

        :param df1: First DataFrame to compare.
        :param df2: Second DataFrame to compare.
        :return: True if both DataFrames are identical, False otherwise.
        """
        # Make copies of the DataFrames to avoid modifying the originals
        df1_copy = df1.copy()
        df2_copy = df2.copy()

        # Sort both DataFrames by the index
        df1_sorted = df1_copy.sort_index()
        df2_sorted = df2_copy.sort_index()

        # Reset index if you want to ignore the index in your comparison
        df1_sorted.reset_index(drop=True, inplace=True)
        df2_sorted.reset_index(drop=True, inplace=True)

        # Check if both DataFrames are identical
        return df1_sorted.equals(df2_sorted)
