import unittest
from unittest.mock import patch
from urllib.error import HTTPError

import pandas as pd
from pandas import Timestamp
from resource_service import get_grid_query_date, get_next_day, get_datetime, get_price_data_from_grid


class ResourceServiceTestCase(unittest.TestCase):

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

    @patch('resource_service.get_price_data_by_location')
    def test_get_price_data_from_grid_called_again_on_failure(self, mock_mds_fn):
        mock_mds_fn.side_effect = [HTTPError("test", 404, "", None, None), None]
        grid_query_params, price_data = get_price_data_from_grid()
        # called with fallback (today's) date
        self.assertEqual(get_grid_query_date(pd.to_datetime('today')),
                         grid_query_params['date'])
        # called twice (i.e. second time being callback)
        self.assertEqual(2, mock_mds_fn.call_count)


if __name__ == '__main__':
    unittest.main()
