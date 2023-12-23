from SharedCode.Utils.math_utils import MathUtils
import pandas as pd
import math
import numpy as np


class KernelRegressionStrategy:
    def __init__(self):
        self.bandwidth = 8
        self.exponent = 8
        self.window = 25

    def kernel_regression_df(self, cdf: pd.DataFrame, column:str, index:int, h:int, r:int, window:int):
        curr_weight = 0
        cum_weight = 0
        yhat = 0
        for i in range(0, 2 + window):
            if (i + index) < len(cdf):
                y = cdf.iloc[i + index][column]
                w = math.pow(1 + (math.pow(i, 2) / (math.pow(h, 2) * 2 * r)), -r)
                curr_weight += y * w
                cum_weight += w
                yhat = curr_weight / cum_weight if cum_weight != 0 else 0
        return round(yhat, 2)
    
    
    def calculate_yhat1(self, df:pd.DataFrame, column:str):
        yhat_values = [None] * len(df)
        for i in range(len(df) - self.window - 1):
            yhat_values[i] = self.kernel_regression_df(df, column, i, self.bandwidth, self.exponent, self.window)
        return yhat_values
    
    def calculate_yhat2(self, df:pd.DataFrame, column:str):
        yhat_values = [None] * len(df)
        for i in range(len(df) - self.window - 1):
            yhat_values[i] = self.kernel_regression_df(df, column, i, self.bandwidth - 2, self.exponent, self.window)
        return yhat_values
    
    def get_yhat1_with_signals(self, df:pd.DataFrame, column:str):
        df["yhat1"] = self.calculate_yhat1(df, column)
        df["prev-yhat"] = df["yhat1"].shift(-1)

        df["pyhat"] = np.where(df["yhat1"] >= df["prev-yhat"], df["yhat1"], np.nan)
        df["nyhat"] = np.where(df["yhat1"] < df["prev-yhat"], df["yhat1"], np.nan)
        return df