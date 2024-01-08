import plotly.graph_objects as go
from plotly.subplots import make_subplots
from SharedCode.Utils.constants import Constants
import pandas as pd
from datetime import datetime
import yfinance as yf
from SharedCode.Repository.Logger.logger_service import LoggerService
import numpy as np
from SharedCode.Repository.Cache.redis_cache_service import RedisCacheService
from SharedCode.Utils.utility import FunctionUtils
from SharedCode.Utils.retries import retry_decorator_with_tel_props
telemetry = LoggerService()


    
class StockChart:

    @staticmethod
    def plot_chart_with_yhat(df:pd.DataFrame, ticker:str, timeframe:str):
        # Set up the subplot structure
        fig = make_subplots(
            rows=2, 
            cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.01, 
            row_heights=[0.9, 0.3]
        )

        # Add the candlestick trace
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="Candle",
            ), row=1, col=1
        )

        # Determine colors based on price change
        colors = [
            Constants.color_red if row["open"] - row["close"] > 0 else Constants.color_green
            for index, row in df.iterrows()
        ]

        # Add the volume bar chart
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df["volume"],
                marker_color=colors,
                showlegend=False
            ),
            row=2,
            col=1,
        )

        # Add pyhat and nyhat traces
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["pyhat"],
                opacity=0.7,
                line=dict(color=Constants.color_green, width=2),
                name="pyhat",
            ), row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["nyhat"],
                opacity=0.7,
                line=dict(color=Constants.color_red, width=2),
                name="nyhat",
            ), row=1, col=1
        )

        # Update the x-axis with the range selector
        fig.update_xaxes(
            rangeselector=dict(
                buttons=list([
                    dict(count=2, label="2D", step="day", stepmode="backward"),
                    dict(count=7, label="7D", step="day", stepmode="backward"),
                    dict(count=14, label="14D", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all"),
                ])
            ), row=1, col=1
        )

        # Update layout to include the title and adjust the range slider visibility
        fig.update_layout(
            title_text=f"{ticker} | {timeframe}",
            height=600,
            width=900,
            xaxis_rangeslider_visible=False,
            xaxis_rangebreaks=[
                dict(bounds=["sat", "mon"]),
                dict(bounds=[15.15, 9.25], pattern="hour"),
            ],
        )

        # Update the y-axes titles
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)

        # Show the figure
        fig.show()
        
    
    

   
    @retry_decorator_with_tel_props(max_retries=3, delay=0.5)
    def generate_chart(self, ticker = "AAPL", period="1y", trend_start = None, trend_end = None,  chart_type = "scatter", point = "Close", stop_price = None, avg_price =None, tel_props=None)-> go.Figure:
        if trend_start:
            trend_start = pd.to_datetime(trend_start)
        if trend_end:
            trend_end = pd.to_datetime(trend_end)
        
        # Ensure trend_start is the earlier date
        if trend_end and (not trend_start or trend_end < trend_start):
            trend_start, trend_end = trend_end, trend_start
        
        # Determine the appropriate period if trend_start is specified
        if trend_start:
            period = self.determine_period(trend_start)
                
        redis_key = FunctionUtils.get_key_for_yfinance(ticker, period)
        cache = RedisCacheService()
        hist = cache.get_decoded_value(redis_key)
        
        if not hist:
            telemetry.info(f"Cache miss, Fetching data from yfinance for ticker: {ticker}, period: {period}", tel_props)
            hist = yf.download(ticker, period = period)
            value = hist.to_json()
            cache.set_value(redis_key, value)
        else:
            telemetry.info(f"Cache hit, Fetched data from cache for ticker: {ticker}, period: {period}", tel_props)
            hist = pd.read_json(hist)

        if chart_type == 'scatter':
            fig = self.create_scatter_chart(hist)
        else:
            fig = self.create_candlestick_chart(hist)

        if trend_start and trend_end:
            df = hist.loc[(hist.index == trend_start) | (hist.index == trend_end)]
            fig = self.add_trend_line(fig, hist, trend_start, trend_end, point, df)

        if stop_price:
            fig = self.add_stop_price_line(fig, hist, stop_price)

        if avg_price:    
            fig = self.add_avg_price_line(fig, hist, avg_price)

        return fig
    

    def determine_period(self, trend_start):
        today = pd.to_datetime(datetime.today().strftime('%Y-%m-%d'))
        days_difference = (today - trend_start).days

        if days_difference <= 365: 
            return '1y'
        elif days_difference <= 730:
            return '2y'
        elif days_difference <= 1825:
            return '5y'
        else:
            return 'max'

    def create_scatter_chart(self, hist):
        return go.Figure(data=go.Scatter(x=hist.index, y=hist['Close'], mode='lines'))

    def create_candlestick_chart(self, hist):
        return go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])

    def add_trend_line(self, fig, hist, trend_start, trend_end, point, df):
        if trend_start and trend_end:
                x = [hist.index.get_loc(trend_start), hist.index.get_loc(trend_end)]
                y = df[point].tolist()
                slope, intercept = np.polyfit(x, y, 1)

                x_val_index = hist.index.get_loc(hist.index[-1])
                y_val = slope * x_val_index + intercept

                fig.add_trace(go.Scatter(
                    x=df.index, y=df[point], mode='markers', marker=dict(size=10)))

                fig.add_shape(type="line",
                              x0=trend_start, y0=slope * x[0] + intercept,
                              x1=hist.index[-1], y1=y_val,
                              line=dict(color='red', width=3))
                
                return fig

    def add_stop_price_line(self, fig, hist, stop_price):
        fig.add_shape(type="line", x0=hist.index[0], y0=stop_price, x1=hist.index[-1], y1=stop_price, line=dict(color='red', width=2), showlegend=True, label=dict(text="SL", textposition="end"))

        return fig

    def add_avg_price_line(self, fig, hist, avg_price):
        fig.add_shape(type="line", x0=hist.index[0], y0=avg_price, x1=hist.index[-1], y1=avg_price, line=dict(color='green', width=2), showlegend=True, name="avg_price")

        return fig


    # Example usage:
    # df = your dataframe with stock data
    # chart = StockChart(df, 'AAPL', '1D')
    # chart.plot()




    # df['MA20'] = df['close'].rolling(window=20).mean()
    # df['MA5'] = df['close'].rolling(window=5).mean()
