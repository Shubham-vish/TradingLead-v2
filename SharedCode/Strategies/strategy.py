from datetime import datetime, timedelta
import math
from lib.config import ticker_name, tf
from logs.logging import logger, logging

lookback_window = 8
relative_weighting = 8
start_regression_bar = 25
lag = 2
smooth_colors = False




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