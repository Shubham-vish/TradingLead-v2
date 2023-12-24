import math
import pandas as pd
class MathUtils:
    @staticmethod
    def kernel_regression(src, h, r, x_0):
        curr_weight = 0
        cum_weight = 0
        yhat = 0
        for i in range(0,2+x_0):
            y = src[i]
            # Handle cases where the index is out of range
            # print("y",y, " ",i)
            w = math.pow(1 + (math.pow(i, 2) / (math.pow(h, 2) * 2 * r)), -r)
            curr_weight += y * w
            cum_weight += w
            # print("cur w",curr_weight)
            # print("cu ww",cum_weight)

            yhat=curr_weight / cum_weight
            # print("yhat ",yhat)
        return yhat
    