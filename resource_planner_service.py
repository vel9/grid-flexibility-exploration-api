import math
import pandas as pd


def get_n_windows_with_lowest_price(resource,
                                    data_by_location: pd.DataFrame,
                                    num_windows: int,
                                    num_minutes_in_interval: int):
    col_name: str = "Rolling Average"
    allocated = []
    data_by_location_copy = data_by_location.copy()
    window_size = get_window_size(resource.hours, num_minutes_in_interval)

    # add a column representing rolling average ending at given column
    data_by_location_copy[col_name] = get_average(data_by_location_copy, window_size)
    rows_with_min_rolling_avg = data_by_location_copy.nsmallest(num_windows, col_name).values.tolist()
    for idx in range(len(rows_with_min_rolling_avg)):
        row = rows_with_min_rolling_avg[idx]
        end_time = row[0]
        start_time = end_time - pd.Timedelta(hours=(resource.hours - 1))
        rolling_avg_value = row[3]
        name = "Window " + str(idx + 1)
        allocated.append([name, start_time, rolling_avg_value])
        allocated.append([name, end_time, rolling_avg_value])

    return allocated


def get_average(data_by_location, window_size):
    return data_by_location["LMP"].rolling(window=window_size).mean(numeric_only=True).round(decimals=2)


def schedule_resources_in_lowest_price_windows(resources: list,
                                               data_by_location: pd.DataFrame,
                                               num_minutes_in_interval: int):
    col_name: str = "Rolling Average"
    allocated = []
    for resource in resources:
        data_by_location_copy = data_by_location.copy()
        window_size = get_window_size(resource.hours, num_minutes_in_interval)
        # add a column representing rolling average ending at given column
        data_by_location_copy[col_name] = get_average(data_by_location_copy, window_size)

        min_df = data_by_location_copy.min()
        rows_with_min_rolling_avg = data_by_location_copy[data_by_location_copy[col_name] == min_df[col_name].min()]

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
