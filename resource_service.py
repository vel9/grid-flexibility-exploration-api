from chart_data_provider import get_chart_data
from market_data_service import get_price_data_by_location
from resource_data_service import query_resource_by_id, query_all_resources
from price_window_provider import get_lowest_price_window_for_each_resource, get_n_windows_with_lowest_price


def get_resources_and_lowest_price_windows():
    chart, table_data, grid_query = get_lowest_price_windows(query_all_resources())
    return {
        'resources': get_resources_as_dict(),
        'chart': chart,
        'table': table_data,
        'query': grid_query
    }


def get_resource_and_lowest_price_windows(resource_id: str):
    num_windows = 5
    resource = query_resource_by_id(resource_id)
    chart, table, grid_query = get_n_lowest_prices_windows_for_resource(resource, num_windows)
    return {
        'resource': resource.as_dict(),
        'chart': chart,
        'table': table,
        'query': grid_query
    }


def get_resources_as_dict():
    result = []
    resources = query_all_resources()
    for resource in resources:
        result.append(resource.as_dict())
    return result


def get_lowest_price_window_for_resources():
    return get_lowest_price_windows(query_all_resources())


def get_lowest_price_windows(resources):
    num_mins_in_interval = 60
    grid_query_params = get_grid_query_parameters()
    price_data = get_price_data_by_location(grid_query_params)
    lowest_price_windows = get_lowest_price_window_for_each_resource(resources,
                                                                     price_data,
                                                                     num_mins_in_interval)

    return get_chart_data(lowest_price_windows, price_data, grid_query_params)


def get_n_lowest_prices_windows_for_resource(resource, num_windows):
    num_mins_in_interval = 60
    grid_query_params = get_grid_query_parameters()
    price_data = get_price_data_by_location(grid_query_params)
    lowest_price_windows = get_n_windows_with_lowest_price(resource,
                                                           price_data,
                                                           num_windows,
                                                           num_mins_in_interval)

    return get_chart_data(lowest_price_windows, price_data, grid_query_params)


def get_grid_query_parameters():
    return {
        'date': "February 26, 2024",
        'location': "GENESE",
        'market': "DAY_AHEAD_HOURLY",
        'operator': "NYISO"
    }
