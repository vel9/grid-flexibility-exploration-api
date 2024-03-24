import unittest

import pandas as pd
from pandas import Timestamp

from models import Resource
from price_window_provider import get_window_size, get_lowest_price_window_for_each_resource, \
    get_n_windows_with_lowest_price


class ResourcePlannerServiceTestCase(unittest.TestCase):
    def test_get_window_size_by_invalid_num_hours(self):
        with self.assertRaises(ValueError):
            get_window_size(0, 5)

    def test_get_window_size_by_invalid_num_minutes_in_interval(self):
        with self.assertRaises(ValueError):
            get_window_size(5, 0)

    def test_get_window_size_by_whole_hour(self):
        self.assertEqual(12, get_window_size(1, 5))
        self.assertEqual(24, get_window_size(2, 5))

    def test_schedule_resources_in_lowest_price_windows(self):
        resources = [
            Resource("123", "A",  2),
        ]
        slots = []
        for interval in range(24):
            slots.append([Timestamp('20240308') + pd.Timedelta(hours=interval), 17])
        slots[23][1] = 5  # force last window to be optimal

        slots_df = pd.DataFrame(slots, columns=["Time", "LMP"])
        num_mins_in_interval = 60
        result = get_lowest_price_window_for_each_resource(resources, slots_df, num_mins_in_interval)
        # make sure we select our last generated timestamp as end of optimal window
        self.assertEqual(get_timestamp(23), result[1][1])
        # 11 + 11 / 2 = 11
        self.assertEqual(11, result[1][2])

    def test_get_n_windows_with_lowest_price(self):
        resource = Resource("123", "A",  2)
        slots = []
        for interval in range(24):
            slots.append([get_timestamp(interval), "GENESE", 10])
        # force low prices
        slots[10][2] = 4
        slots[22][2] = 6
        slots[23][2] = 2

        slots_df = pd.DataFrame(slots, columns=["Time", "Location", "LMP"])
        num_mins_in_interval = 60
        num_windows = 4
        result = get_n_windows_with_lowest_price(resource,
                                                 slots_df,
                                                 num_windows,
                                                 num_mins_in_interval)

        self.assertEqual(8, len(result))
        self.assert_window_values("Window 1", 4, 23, result[1])
        self.assert_window_values("Window 2", 7, 10, result[3])
        self.assert_window_values("Window 3", 7, 11, result[5])
        self.assert_window_values("Window 4", 8, 22, result[7])

    def assert_window_values(self, expected_name, expected_avg, expected_hour, endpoint):
        self.assertEqual(expected_name, endpoint[0])
        self.assertEqual(get_timestamp(expected_hour), endpoint[1])
        self.assertEqual(expected_avg, endpoint[2])


def get_timestamp(add_hours):
    return Timestamp('20240308') + pd.Timedelta(hours=add_hours)


if __name__ == '__main__':
    unittest.main()
