import unittest

from pandas import Timestamp
from resource_service import get_grid_query_date, get_next_day


class ResourceServiceCase(unittest.TestCase):

    def test_get_grid_query_date(self):
        self.assertEqual('February 26, 2024', get_grid_query_date(Timestamp('20240226')))

    def test_get_next_day(self):
        self.assertEqual(Timestamp('20240226'), get_next_day(Timestamp('20240225')))


if __name__ == '__main__':
    unittest.main()