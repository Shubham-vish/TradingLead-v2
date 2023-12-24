from datetime import datetime, timedelta
import pandas as pd


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
    def get_storage_ticker(ticker):
        return ticker.replace(":", "_")

    @staticmethod
    def filter_last_n_days(df, n=20):
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
    def resample_to_timeframe(df, frequency="30T"):
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
    def are_dataframes_identical(df1, df2):
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
