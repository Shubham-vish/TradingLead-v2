from .blob_service_factory import BlobServiceFactory
import pandas as pd
from io import StringIO, BytesIO
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils


class BlobService:
    def __init__(self):
        self.client = BlobServiceFactory.get_blob_service_client()

    def get_blob_client(self, container_name, blob_name):
        return self.client.get_blob_client(container=container_name, blob=blob_name)

    def get_container_client(self, container_name):
        return self.client.get_container_client(container_name)

    def get_blob_to_stream(self, container_name, blob_name):
        blob_client = self.get_blob_client(container_name, blob_name)
        return blob_client.download_blob()

    def download_blob_to_file(self, container_name, blob_name, file_path):
        blob_client = self.get_blob_client(container_name, blob_name)
        with open(file=file_path, mode="wb") as sample_blob:
            download_stream = blob_client.download_blob()
            sample_blob.write(download_stream.readall())

    def get_dataframe_from_blob(self, container_name, blob_name):
        blob_client = self.get_blob_client(container_name, blob_name)
        download_stream = blob_client.download_blob()
        txt = download_stream.content_as_text()
        txt_io = StringIO(txt)
        df = pd.read_csv(txt_io)
        return df

    def get_nifty_tickers_historical_df(self, ticker):
        ticker = FunctionUtils.get_storage_ticker(ticker)
        blob_name = f"{Constants.DIR_NIFTY_50}/{ticker}.csv"
        return self.get_dataframe_from_blob(
            Constants.STOCK_HISTORY_CONTAINER, blob_name
        )

    def create_blob(self, df, container_name, blob_name):
        """
        Creates a blob in the specified container with the given name from a DataFrame.

        :param df: DataFrame to be uploaded.
        :param container_name: Name of the Azure Blob Storage container.
        :param blob_name: Name for the blob.
        """

        # Convert DataFrame to CSV format and encode to bytes
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        data = csv_buffer.read()

        # Get a blob client using the container name and blob name
        blob_client = self.get_blob_client(container_name, blob_name)

        # Upload the data to the blob
        blob_client.upload_blob(data, overwrite=True)
