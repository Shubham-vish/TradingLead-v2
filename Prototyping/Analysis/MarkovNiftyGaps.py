# %%
# videoUrl = "https://www.youtube.com/watch?v=gA0egjZcRB0&ab_channel=QuantProgram"
# Markov Process:
    # Sequence -> Probabilities -> FutureState -> CurrentState
    # Tomorrow's weather depends on today's weather
    # Home <=> Shop <=> Work
    
    # Add Markov Trading Probabilities

# %%
import yfinance as yf
import pandas as pd
import numpy as np

# %%
ticker = "^NSEI"
data = yf.download(ticker, start="2010-01-01", end="2022-04-22")


# %%
data

# %%
data["daily_return"] = data["Adj Close"].pct_change()
data["state"] = np.where(data["daily_return"] > 0, "up", "down")


# %%
data

# %%

up_counts = len(data[data["state"] == "up"])
down_counts = len(data[data["state"] == "down"])
up_to_up = len(data[(data["state"] == "up") & (data["state"].shift(-1) == "up") ]) / len(data.query('state=="up"'))
down_to_up = len(data[(data["state"] == "up") & (data["state"].shift(-1) == "down")]) / len(data.query('state=="up"'))
up_to_down = len(data[(data["state"] == "down") & (data["state"].shift(-1) == "up")]) / len(data.query('state=="down"'))
down_to_down = len(data[(data["state"] == "down") & (data["state"].shift(-1) == "down")]) / len(data.query('state=="down"'))
transition_matrix = pd.DataFrame({
    "up": [up_to_up, up_to_down],
    "down": [down_to_up, down_to_down]
}, index=["up", "down"])

print(transition_matrix)

# %%

len(data[(data["state"] == "up") & (data["state"].shift(-1) == "down") & (data["state"].shift(-2) == "down") & (data["state"].shift(-3) == "down") & (data["state"].shift(-4) == "down") & (data["state"].shift(-5) == "down")]) / len(data[(data["state"].shift(1) == "down") & (data["state"].shift(2) == "down") & (data["state"].shift(3) == "down") & (data["state"].shift(4) == "down") & (data["state"].shift(5) == "down")])

# %%
ticker = "^NSEI"
datanifty = yf.download(ticker, start="2010-01-01", end="2022-04-22")


# %%
datanifty


