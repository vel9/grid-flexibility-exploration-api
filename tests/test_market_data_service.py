import unittest
from unittest.mock import patch

from market_data_service import get_price_data_by_location


class MarketDataServiceTestCase(unittest.TestCase):

    @patch('market_data_service.get_data_from_grid')
    def test_get_price_data_by_location_by_cached_value(self, mock_mds_fn):
        params = {'date': "a", 'location': "b", 'market': "c"}
        get_price_data_by_location(params)
        self.assertEqual(1, mock_mds_fn.call_count)
        get_price_data_by_location(params)
        self.assertEqual(1, mock_mds_fn.call_count) # cached result for a
        params['date'] = "b"
        get_price_data_by_location(params)
        self.assertEqual(2, mock_mds_fn.call_count) # but not for b

if __name__ == '__main__':
    unittest.main()
