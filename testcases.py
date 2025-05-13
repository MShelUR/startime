import unittest
from startime import parse_time
from datetime import date, timedelta

today = str(date.today().strftime("%m/%d/%Y"))

class test_cases(unittest.TestCase):
    def test_normal_dates(self):
        for i in range(4000): # does it parity datetime
            assert parse_time(f"*/*+{i}/*") == (date.today() + timedelta(days=i)).strftime("%m/%d/%Y")

    def test_division(self):
        assert parse_time("5/(7/3)/2025") == "05/02/2025" # rounding down
        assert parse_time("5/(23/2)/2025") == "05/12/2025" # rounding up

        with self.assertRaises(ZeroDivisionError): # 0 division is bad!
            parse_time("*/(5/0)/*")

    def test_wrapping(self):
        assert parse_time("1/31+1/2025") == "02/01/2025"
        assert parse_time("1+12/31+1/2025") == "02/01/2026"

    
    def test_grouping_symbols(self):
        assert parse_time("*/*+(5)(3*(2+3))/*") == (date.today() + timedelta(days=75)).strftime("%m/%d/%Y") # valid

        with self.assertRaises(ValueError):
            parse_time("(*/(5))/*") # in different sections of date
        with self.assertRaises(ValueError):
            parse_time("*/((5)/*") # missing closing parenthesis


if __name__ == "__main__":
    unittest.main()