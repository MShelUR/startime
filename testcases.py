import unittest
from startime import parse_time
from datetime import date, timedelta

today = str(date.today().strftime("%m/%d/%Y"))

class test_cases(unittest.TestCase):
    def test_normal_dates(self):
        for i in range(4000): # does it parity datetime
            assert parse_time(f"*/*+{i}/*") == (date.today() + timedelta(days=i)).strftime("%m/%d/%Y")

    def test_zero_division(self):
        with self.assertRaises(ZeroDivisionError):
            parse_time("*/(5/0)/*")
    
    def test_grouping_symbols(self):
        assert parse_time("*/*+(5)(3*(2+3))/*") == (date.today() + timedelta(days=75)).strftime("%m/%d/%Y") # valid

        with self.assertRaises(ValueError):
            parse_time("(*/(5))/*") # in different sections
        with self.assertRaises(ValueError):
            parse_time("*/((5)/*") # missing closing


if __name__ == "__main__":
    unittest.main()