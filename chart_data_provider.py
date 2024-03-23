import pandas as pd


def get_chart_data(allocated_resources_day_ahead, day_ahead_price_data, grid_query):
    return get_plotly_chart_data(allocated_resources_day_ahead, day_ahead_price_data, grid_query)


def get_plotly_chart_data(allocated_resources_day_ahead, day_ahead_price_data, grid_query):
    chart_data_traces = []
    table_data = []
    date_format = "%Y-%m-%d %X"
    for idx in range(0, len(allocated_resources_day_ahead), 2):
        start_point = allocated_resources_day_ahead[idx]
        end_point = allocated_resources_day_ahead[idx + 1]
        chart_data_traces.append(get_chart_data_point(start_point, end_point, date_format))
        table_data.append(get_table_row(start_point, end_point, date_format))

    chart_data_traces.append(get_price_data_trace(day_ahead_price_data, date_format))
    return chart_data_traces, table_data, grid_query


def get_table_row(start_point, end_point, date_format):
    start_time = start_point[1].strftime(date_format)
    end_time = end_point[1].strftime(date_format)
    return {
        'name': start_point[0],
        'start': start_time,
        'end': end_time,
        'average': start_point[2]
    }


def get_price_data_trace(day_ahead_price_data, date_format):
    df = pd.DataFrame(day_ahead_price_data, columns=["Resource", "Time", "LMP"])
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


def get_chart_data_point(start_point, end_point, date_format):
    start_time = start_point[1].strftime(date_format)
    end_time = end_point[1].strftime(date_format)
    return {
        'name': start_point[0],
        'x': [start_time, end_time],
        'y': [start_point[2], end_point[2]],
        'type': "line",
        'mode': "lines+markers"
    }
