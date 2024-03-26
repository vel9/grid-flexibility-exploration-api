from urllib.error import HTTPError

import pandas as pd

from chart_data_provider import get_chart_data
from market_data_service import get_price_data_by_location
from models import Resource
from resource_data_service import query_resource_by_id, query_all_resources
from price_window_provider import get_lowest_price_window_for_each_resource, get_n_windows_with_lowest_price


def get_resources_and_lowest_price_windows():
    """
    Combine resources, chart data, table data and query for
    market data into a single dict

    :return: dict of resources and associated data
    """
    resources = query_all_resources()
    chart, table_data, grid_query = get_lowest_price_windows(resources)
    return {
        'resources': get_resources_as_dict(resources),
        'chart': chart,
        'table': table_data,
        'query': grid_query
    }


def get_resource_and_lowest_price_windows(resource_id: str):
    """
    Combine single resource, chart data, table data and query for
    market data into a single dict

    Retrieves num_windows best/lowest windows for the resource

    :param resource_id: resource unique id
    :return: dict of resource and associated data
    """
    num_windows = 5
    resource = query_resource_by_id(resource_id)
    chart, table, grid_query = get_n_lowest_prices_windows_for_resource(resource, num_windows)
    return {
        'resource': resource.as_dict(),
        'chart': chart,
        'table': table,
        'query': grid_query
    }


def get_resources_as_dict(resources: list[Resource]):
    """
    Convert resource objects to dicts

    :param resources: list of resources objs
    :return: list of dicts
    """
    result = []
    for resource in resources:
        result.append(resource.as_dict())
    return result


def get_lowest_price_window_for_resources():
    return get_lowest_price_windows(query_all_resources())


def get_lowest_price_windows(resources: list[Resource], num_mins_in_interval: int = 60):
    """
    Get lowest price window for each resource and structure it
    for chart display

    :param resources: list of resources
    :param num_mins_in_interval: minutes in price interval
    :return: data structured for chart display
    """
    grid_query_params, price_data = get_price_data_from_grid()
    lowest_price_windows = get_lowest_price_window_for_each_resource(resources,
                                                                     price_data,
                                                                     num_mins_in_interval)

    return get_chart_data(lowest_price_windows, price_data, grid_query_params)


def get_n_lowest_prices_windows_for_resource(resource: Resource,
                                             num_windows: int,
                                             num_mins_in_interval: int = 60):
    """
    Get n lowest price windows for single resource and structure it
    for chart display

    :param resource: list of resources
    :param num_windows: number of best/lowest price windows
    :param num_mins_in_interval: minutes in price interval
    :return: data structured for chart display
    """
    grid_query_params, price_data = get_price_data_from_grid()
    lowest_price_windows = get_n_windows_with_lowest_price(resource,
                                                           price_data,
                                                           num_windows,
                                                           num_mins_in_interval)

    return get_chart_data(lowest_price_windows, price_data, grid_query_params)


def get_price_data_from_grid():
    """
    Query grid with tomorrow's day for day ahead prices
    It's possible prices for tomorrow are not yet published
    If so, fall back to using today's prices

    :return: query used and related price data
    """
    try:
        grid_query_params = get_grid_query_parameters("tomorrow")
        price_data = get_price_data_by_location(grid_query_params)
    except HTTPError:
        grid_query_params = get_grid_query_parameters("today")
        grid_query_params['fallback'] = True
        price_data = get_price_data_by_location(grid_query_params)

    return grid_query_params, price_data


def get_grid_query_parameters(date_type: str):
    """
    Provide query for grid market data
    Requests prices for day ahead (i.e. tomorrow)

    :param date_type: get date given provided date type
    :return: grid query parameters
    """
    return {
        'date': get_grid_query_date(get_datetime(date_type)),
        'location': "GENESE",
        'market': "DAY_AHEAD_HOURLY",
        'operator': "NYISO",
        'fallback': False
    }


def get_datetime(date_type: str):
    """
    Add day to current date if date_type is tomorrow

    :param date_type: get date given provided date type
    :return: datetime
    """
    if date_type == "tomorrow":
        return get_next_day(pd.to_datetime('today'))
    else:
        return pd.to_datetime('today')


def get_grid_query_date(date_time: pd.Timestamp):
    """
    Format timestamp as 'February 26, 2024'

    :param date_time: timestamp to format
    :return: formatted date
    """
    return date_time.strftime("%B %d, %Y")


def get_next_day(date_time: pd.Timestamp):
    """
    Add 1 day to provided timestamp

    :param date_time: timestamp
    :return: timestamp with one day added
    """
    return date_time + pd.Timedelta(days=1)
