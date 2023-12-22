from SharedCode.Utils.math_utils import MathUtils


class KernelRegressionStrategy:
    def __init__(self):
        self.lookback_window = 8
        self.relative_weighting = 8
        self.x_0 = 25
        self.lag = 2
        self.smooth_colors = False

    def get_order_signal(self, close_prices, position):

        signal = 0
        _src = close_prices[::-1]
        _src = _src[:30]
        c_cp = _src[0]
        # print("r cp data ",_src)
        yhat1 = self.getyaht1(_src)

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
    
    def get_yhat1(self, close_prices):

        _src = close_prices[::-1]
        _src = _src[:30]
        # print("r cp data ",_src)
        yhat1 = MathUtils.kernel_regression(_src, self.lookback_window, self.relative_weighting, self.x_0)
        return yhat1