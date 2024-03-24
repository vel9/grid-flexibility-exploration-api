import pandas as pd


def get_chart_data(lowest_price_windows, price_data, grid_query):
    """
    Get formatted/structured data for chart display

    :param lowest_price_windows: windows within price data
    :param price_data: price data from grid
    :param grid_query: query used for querying grid
    :return: chart data
    """
    return get_plotly_chart_data(lowest_price_windows, price_data, grid_query)


def get_plotly_chart_data(lowest_price_windows, day_ahead_price_data, grid_query):
    """
    Get formatted data for plotly js

    :param lowest_price_windows: windows within price data
    :param price_data: price data from grid
    :param grid_query: query used for querying grid
    :return: chart data
    """
    chart_data_traces = []
    table_data = []
    date_format = "%Y-%m-%d %X"
    for idx in range(0, len(lowest_price_windows), 2):
        start_point = lowest_price_windows[idx]
        end_point = lowest_price_windows[idx + 1]
        chart_data_traces.append(get_window_trace(start_point, end_point, date_format))
        table_data.append(get_table_row(start_point, end_point, date_format))

    chart_data_traces.append(get_price_data_trace(day_ahead_price_data, date_format))
    return chart_data_traces, table_data, grid_query


def get_table_row(start_point, end_point, date_format):
    """
    Get data for table row

    :param start_point: window start
    :param end_point: window end
    :param date_format: formatter
    :return: table row data
    """
    start_time = start_point[1].strftime(date_format)
    end_time = end_point[1].strftime(date_format)
    return {
        'name': start_point[0],
        'start': start_time,
        'end': end_time,
        'average': start_point[2]
    }


def get_price_data_trace(price_data, date_format):
    """
    Format price data for plotly, reformat date

    :param price_data: grid price data
    :param date_format: date format for plotly
    :return: price data trace
    """
    df = pd.DataFrame(price_data, columns=["Resource", "Time", "LMP"])
    times = df["Time"].tolist()
    prices = df["LMP"].tolist()
    for idx in range(len(times)):
        times[idx] = times[idx].strftime(date_format)
    return {
        'name': "Day Ahead Price",
        'x': times,
        'y': prices,
        'type': "line",
        'mode': "lines",
        'marker': {'color': "#0dcaf0"}
    }


def get_window_trace(start_point, end_point, date_format):
    """
    Get trace for resource window

    :param start_point: window start
    :param end_point: window end
    :param date_format: date format for plotly
    :return: trace object for window
    """
    start_time = start_point[1].strftime(date_format)
    end_time = end_point[1].strftime(date_format)
    return {
        'name': start_point[0],
        'x': [start_time, end_time],
        'y': [start_point[2], end_point[2]],
        'type': "line",
        'mode': "lines+markers"
    }
