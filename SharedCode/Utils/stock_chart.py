import plotly.graph_objects as go
from plotly.subplots import make_subplots
from SharedCode.Utils.constants import Constants
import pandas as pd

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


# Example usage:
# df = your dataframe with stock data
# chart = StockChart(df, 'AAPL', '1D')
# chart.plot()




# df['MA20'] = df['close'].rolling(window=20).mean()
# df['MA5'] = df['close'].rolling(window=5).mean()
