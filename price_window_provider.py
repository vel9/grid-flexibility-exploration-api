import math
import pandas as pd

from models import Resource


def get_n_windows_with_lowest_price(resource: Resource,
                                    price_data: pd.DataFrame,
                                    num_windows: int,
                                    num_minutes_in_interval: int):
    """
    Get n windows with lowest average price within price data

    :param resource: resource for which we're getting lowest windows
    :param price_data: price data
    :param num_windows: number of windows
    :param num_minutes_in_interval: number of minutes in each price interval
    :return: windows with lowest price
    """
    col_name: str = "Rolling Average"
    allocated = []
    price_data_copy = price_data.copy()
    window_size = get_window_size(resource.hours, num_minutes_in_interval)

    # add a column representing rolling average ending at given column
    price_data_copy[col_name] = get_average(price_data_copy, window_size)
    rows_with_min_rolling_avg = price_data_copy.nsmallest(num_windows, col_name).values.tolist()
    for idx in range(len(rows_with_min_rolling_avg)):
        row = rows_with_min_rolling_avg[idx]
        end_time = row[0]
        start_time = end_time - pd.Timedelta(hours=(resource.hours - 1))
        rolling_avg_value = row[3]
        name = "Window " + str(idx + 1)
        allocated.append([name, start_time, rolling_avg_value])
        allocated.append([name, end_time, rolling_avg_value])

    return allocated


def get_average(price_data: pd.DataFrame, window_size: int):
    """
    Helper function for calculating rolling average for price

    :param price_data: price data
    :param window_size: number of rows in window
    :return: rolling average column with values
    """
    return price_data["LMP"].rolling(window=window_size).mean(numeric_only=True).round(decimals=2)


def get_lowest_price_window_for_each_resource(resources: list,
                                              price_data: pd.DataFrame,
                                              num_minutes_in_interval: int):
    """
    For each resource find the single lowest/best price window

    :param resources: list of resources
    :param price_data: price data
    :param num_minutes_in_interval: number of minutes in each price interval
    :return:
    """
    col_name: str = "Rolling Average"
    allocated = []
    for resource in resources:
        price_data_copy = price_data.copy()
        window_size = get_window_size(resource.hours, num_minutes_in_interval)
        # add a column representing rolling average ending at given column
        price_data_copy[col_name] = get_average(price_data_copy, window_size)

        min_df = price_data_copy.min()
        rows_with_min_rolling_avg = price_data_copy[price_data_copy[col_name] == min_df[col_name].min()]

        # only get end time from first matching window
        end_time = rows_with_min_rolling_avg["Time"].iloc[0]
        start_time = end_time - pd.Timedelta(hours=(resource.hours - 1))
        rolling_avg_value = rows_with_min_rolling_avg[col_name].iloc[0]

        allocated.append([resource.name, start_time, rolling_avg_value])
        allocated.append([resource.name, end_time, rolling_avg_value])

    return allocated


def get_window_size(num_hours: int, num_minutes_in_interval: int):
    """
    Break hours down into intervals

    :param num_hours: number of hours
    :param num_minutes_in_interval: sample size
    :return: number of 5 minute intervals in num_hours
    """
    if num_hours <= 0:
        raise ValueError("num_hours must be greater than 0")
    if num_minutes_in_interval <= 0:
        raise ValueError("num_minutes_in_interval must be greater than 0")
    return math.ceil((num_hours * 60) / num_minutes_in_interval)
