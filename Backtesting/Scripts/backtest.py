import os
import sys

# Below code is for testing
sys.path.append(os.path.abspath(os.path.join("../..")))

from Notebooks.setupConfig import setup_config

setup_config()

# Above code is for testing

import pandas as pd

from SharedCode.Repository.BlobService.blob_service import BlobService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.tikers import Tickers
from SharedCode.Utils.utility import FunctionUtils

blob_service = BlobService()

df = blob_service.get_ticker_history(Tickers.nifty_50_stocks[0])

fdf = FunctionUtils.filter_last_n_days(20)
