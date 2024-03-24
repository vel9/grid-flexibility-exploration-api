import unittest

import validator


class ValidatorTestCase(unittest.TestCase):

    def test_validate_add_resource_by_empty_name(self):
        result = validator.validate_add_resource("", "1")
        self.assertEqual(True, result.has_errors)  # add assertion here
        self.assertEqual(result.errors['name'], "Name must not be empty")

    def test_validate_add_resource_by_empty_hour(self):
        result = validator.validate_add_resource("test", "")
        self.assertEqual(True, result.has_errors)  # add assertion here
        self.assertEqual(result.errors['hours'], "Hour must not be empty")

    def test_validate_add_resource_by_invalid_hour_type(self):
        result = validator.validate_add_resource("test", "a")
        self.assertEqual(True, result.has_errors)  # add assertion here
        self.assertEqual(result.errors['hours'], "Hour must be an integer")

    def test_validate_add_resource_by_invalid_hour_bound(self):
        out_of_bound_message = "Hour must be between 1 and 23"

        result = validator.validate_add_resource("test", "0")
        self.assertEqual(True, result.has_errors)  # add assertion here
        self.assertEqual(result.errors['hours'], out_of_bound_message)

        result = validator.validate_add_resource("test", "24")
        self.assertEqual(True, result.has_errors)  # add assertion here
        self.assertEqual(result.errors['hours'], out_of_bound_message)


if __name__ == '__main__':
    unittest.main()
