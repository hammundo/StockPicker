import pandas as pd
import numpy as np
import yfinance as yf

from datetime import date
from datetime import datetime
from datetime import timedelta


def fetch_ticker(ticker: str, time_range: str, interval: str) -> pd.DataFrame:
    forex_data = yf.Ticker(ticker).history(period=time_range, interval=interval)
    forex_data.drop(
        ['Volume', 'Dividends', 'Stock Splits'],
        axis=1,
        inplace=True
    )

    forex_data.reset_index(inplace=True)
    forex_data.rename(columns={'index': 'Datetime'}, inplace=True)
    return forex_data


# TODO: Use numpy/pandas built in methods such as iloc / window
def is_support(df: pd.DataFrame, i: int) -> tuple:
    support = df['Low'][i] < df['Low'][i - 1] and df['Low'][i] < df['Low'][i + 1] < df['Low'][i + 2] and df['Low'][i - 1] < df['Low'][i - 2]
    return support


# TODO: Use numpy/pandas built in methods such as iloc / window
def is_resistance(df: pd.DataFrame, i: int) -> tuple:
    resistance = df['High'][i] > df['High'][i - 1] and df['High'][i] > df['High'][i + 1] > df['High'][i + 2] and df['High'][i - 1] > df['High'][i - 2]
    return resistance


def convert_to_pydatetime(x) -> str:
    timestamp = x.to_pydatetime()
    str_timestamp = str(timestamp)
    return str_timestamp


def create_level_coords(data: pd.DataFrame):
    support_levels = []
    resistance_levels = []

    for i in range(2, data.shape[0] - 2):
        if is_support(data, i):
            timestamp = convert_to_pydatetime(data['Datetime'][i])
            support_levels.append((timestamp, data['Low'][i]))
        elif is_resistance(data, i):
            timestamp = convert_to_pydatetime(data['Datetime'][i])
            resistance_levels.append((timestamp, data['High'][i]))

    # Split resistance tuples into 2 lists.
    support_result = (map(list, zip(*support_levels)))
    support_x, support_y = support_result

    resistance_result = (map(list, zip(*resistance_levels)))
    resistance_x, resistance_y = resistance_result

    # Add an offset to the Y values so that when markers are plotted they do not block the candlesticks
    new_res_y = []
    for value in resistance_y:
        i = value + 0.015
        new_res_y.append(i)

    new_sup_y = []
    for value in support_y:
        i = value - 0.015
        new_sup_y.append(i)

    levels = {'Support X': support_x, 'Support Y': new_sup_y, 'Resistance X': resistance_x, 'Resistance Y': new_res_y}
    return levels


test_ticker = 'USDGBP=X'
test_time_range = '2wk'
test_interval = '60m'
test_strength = 2

df = pd.DataFrame(data=fetch_ticker(test_ticker, test_time_range, test_interval))
support_df = is_support(df, test_strength)
resistance_df = is_resistance(df, test_strength)
levels_df = create_level_coords(df)

print(levels_df)
