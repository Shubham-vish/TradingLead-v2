from SharedCode.Utils.math_utils import MathUtils


class KernelRegressionStrategy:
    def __init__(self):
        self.lookback_window = 8
        self.relative_weighting = 8
        self.start_regression_bar = 25
        self.lag = 2
        self.smooth_colors = False

    def get_order_signal(self, close_prices, position):

        signal = 0
        r_cp = close_prices[::-1]
        r_cp = r_cp[:30]
        c_cp = r_cp[0]
        # print("r cp data ",r_cp)
        yhat1 = MathUtils.kernel_regression(r_cp, self.lookback_window, self.relative_weighting, self.start_regression_bar)
        yhat2 = MathUtils.kernel_regression(r_cp, self.lookback_window - self.lag, self.relative_weighting, self.start_regression_bar)

        print("C_cp : ",c_cp )
        print("yhat1 : ",yhat1)
        print("yhat2 : ",yhat2)
        # if(c_cp > yhat2 and c_cp < yhat1):
        #   signal = 0
        if(c_cp > yhat1 and position==0):
            signal=1
        elif(c_cp < yhat1 and position==1):
            signal = -1
        else:
            signal=0

        return signal
       