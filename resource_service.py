import uuid

from chart_data_provider import get_chart_data
from database import init_db, db_session
from market_data_service import get_price_data_by_location
from models import Resource
from resource_planner_service import schedule_resources_in_lowest_price_windows, get_n_windows_with_lowest_price


def get_all_resources():
    init_db()
    return Resource.query.all()


def get_all_resource(resource_id: str):
    resource = Resource.query.get(resource_id)
    chart, table, grid_query = plan_resource_day_ahead(resource)
    return {
        "resource": resource.as_dict(),
        "chart": chart,
        "table": table,
        "query": grid_query
    }


def get_all_resources_as_dict():
    result = []
    resources = get_all_resources()
    for resource in resources:
        result.append(resource.as_dict())
    return result


def get_planned_resources():
    return plan_resources_day_ahead(get_all_resources())


def add_resource_to_db(name: str, hours: int):
    resource = Resource(str(uuid.uuid4()), name, hours)
    db_session.add(resource)
    db_session.commit()
    return "200"


def delete_resource_from_db(id_to_delete: str):
    Resource.query.filter_by(unique_id=id_to_delete).delete()
    db_session.commit()
    return "200"


def plan_resources_day_ahead(resources):
    num_mins_in_interval = 60
    grid_query_params = get_grid_query_parameters()
    day_ahead_price_data = get_price_data_by_location(grid_query_params["date"],
                                                      grid_query_params["location"],
                                                      grid_query_params["market"])
    allocated_resources_day_ahead = schedule_resources_in_lowest_price_windows(resources,
                                                                               day_ahead_price_data,
                                                                               num_mins_in_interval)

    return get_chart_data(allocated_resources_day_ahead, day_ahead_price_data, grid_query_params)


def plan_resource_day_ahead(resource):
    num_mins_in_interval = 60
    num_windows = 5
    grid_query_params = get_grid_query_parameters()
    day_ahead_price_data = get_price_data_by_location(grid_query_params["date"],
                                                      grid_query_params["location"],
                                                      grid_query_params["market"])

    allocated_resources_day_ahead = get_n_windows_with_lowest_price(resource,
                                                                    day_ahead_price_data,
                                                                    num_windows,
                                                                    num_mins_in_interval)

    return get_chart_data(allocated_resources_day_ahead, day_ahead_price_data, grid_query_params)


def get_grid_query_parameters():
    return {
        "date": "February 26, 2024",
        "location": "GENESE",
        "market": "DAY_AHEAD_HOURLY",
        "operator": "NYISO"
    }