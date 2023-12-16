from datetime import datetime, timedelta
import math
from lib.config import ticker_name, tf
from logs.logging import logger, logging

lookback_window = 8
relative_weighting = 8
start_regression_bar = 25
lag = 2
smooth_colors = False


# Define a custom kernel regression function
def kernel_regression(src, h, r, x_0):
    try:
        _currentWeight = 0
        _cumulativeWeight = 0
        yhat = 0

        for i in range(0,2+x_0):
            y = src[i]
            # Handle cases where the index is out of range
            # print("y",y, " ",i)
            w = math.pow(1 + (math.pow(i, 2) / ((math.pow(h, 2) * 2 * r))), -r)
            _currentWeight += y * w
            _cumulativeWeight += w
            # print("cur w",_currentWeight)
            # print("cu ww",_cumulativeWeight)

            yhat=_currentWeight / _cumulativeWeight
            # print("yhat ",yhat)
        return yhat
    except:
        logger.warning("kernel_regression")

def get_hour_close_data():
    try:
        from main import fyers
        data = {
            "symbol":ticker_name,
            "resolution":tf,
            "date_format":"1",
            "range_from":"2023-10-10",
            "range_to":"2023-12-30",
            "cont_flag":"1"
        }

        response = fyers.history(data=data)
        print("Api response :",response["s"])
        candles = response["candles"]
        close_prices = [candle[-2] for candle in candles]
        stoploss = response["candles"][-1][-3]
        return close_prices
    except:
        logger.warning("get_hour_close_data")

def get_order_signal(close_prices,position):

    try:
        signal = 0
        r_cp = close_prices[::-1]
        r_cp = r_cp[:30]
        c_cp = r_cp[0]
        # print("r cp data ",r_cp)
        yhat1 = kernel_regression(r_cp, lookback_window, relative_weighting, start_regression_bar)
        yhat2 = kernel_regression(r_cp, lookback_window - lag, relative_weighting, start_regression_bar)

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
    except:
        logger.warning("get_order_signal")

def get_trades_time():


    try:
        start_time_str = "09:14"
        end_time_str = "15:31"

        # Convert the time strings to datetime objects
        start_time = datetime.strptime(start_time_str, "%H:%M")
        end_time = datetime.strptime(end_time_str, "%H:%M")
        time_list=["15:28"]
        while(start_time < end_time):
            # Convert the start time string to a datetime object
            time_difference = timedelta(minutes=int(tf))
            # Add the time difference to the current time
            new_time = start_time + time_difference
            
            # Format the new time in 24-hour format (HH:MM)
            trade_time = new_time.strftime("%H:%M")
            time_list.append(trade_time)
            start_time = datetime.strptime(trade_time, "%H:%M")
        
        return time_list
    
    except:
        logger.error("error in get_trades_time")