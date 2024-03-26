import gridstatus

cache = {}


def get_price_data_by_location(grid_query_params):
    date = grid_query_params['date']
    location = grid_query_params['location']
    market = grid_query_params['market']
    if date in cache:
        return cache[date]
    data = get_data_from_grid(date, location, market)
    cache[date] = data
    return data


def get_data_from_grid(date, location, market):
    lmp = gridstatus.NYISO().get_lmp(date=date, market=market)
    lmp_col_subset = lmp[["Time", "Location", "LMP"]]
    lmp_subset_filtered = lmp_col_subset[lmp_col_subset["Location"] == location]
    return lmp_subset_filtered
