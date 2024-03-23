import pandas as pd
from pandas import Timestamp

market_data = [

]

def get_price_data_by_location(grid_query_params):
    date = grid_query_params["date"]
    location = grid_query_params["location"]
    market = grid_query_params["market"]
    for iter in range(len(market_data)):
        market_data[iter][1] = Timestamp('20240226') + pd.Timedelta(hours=iter)
    lmp = pd.DataFrame(market_data, columns=["Id","Time", "Location", "LMP"])
    lmp_col_subset = lmp[["Time", "Location", "LMP"]]
    lmp_subset_filtered = lmp_col_subset[lmp_col_subset["Location"] == location]
    return lmp_subset_filtered
