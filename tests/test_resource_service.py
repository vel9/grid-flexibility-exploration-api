import unittest

import pandas as pd
from pandas import Timestamp
from resource_service import get_grid_query_date, get_next_day, get_datetime


class ResourceServiceCase(unittest.TestCase):

    def test_get_grid_query_date(self):
        self.assertEqual('February 26, 2024', get_grid_query_date(Timestamp('20240226')))

    def test_get_next_day(self):
        self.assertEqual(Timestamp('20240226'), get_next_day(Timestamp('20240225')))

    def test_get_query_date_by_today_type(self):
        self.assertEqual(get_grid_query_date(pd.to_datetime('today')),
                         get_grid_query_date(get_datetime("today")))

    def test_get_query_date_by_tomorrow_type(self):
        self.assertEqual(get_grid_query_date(pd.to_datetime('today') + pd.Timedelta(days=1)),
                         get_grid_query_date(get_datetime("tomorrow")))

if __name__ == '__main__':
    unittest.main()