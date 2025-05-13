import sys
from datetime import date

def add(a: int, b: int) -> int:
    return a+b
def sub(a: int, b: int) -> int:
    return a-b
def mult(a: int, b: int) -> int:
    return int(a*b)
def div(a: int, b: int) -> int:
    return int(a/b)

math_symbols = {'+': add, '-': sub, '*': mult, '/': div}

def is_leap_year(year: int) -> bool:
    return year%4 == 0 and (year%100 != 0 or year%400 == 0)

days_in_month = [0,31,28,31,30,31,30,31,31,30,31,30,31]
def get_days_in_month(month: int, year: int) -> bool:
    return days_in_month[month] + int(is_leap_year(year) and month == 2)

def parse_time(inp: str) -> str:
    # get dates
    today = date.today().strftime("%m/%d/%y").split("/")
    split_input = inp.split("/")
    if len(split_input) != 3:
        raise ValueError("Valid date must be of m/d/y format")

    # reformat '*' to current value
    for i in range(3):
        # split input into tree until all leaf nodes are definite ints, edges are operations
        #   ambiguity between * as multiplication and * as current day
        #   valid operator must have two targets, split into two operands and prioritize pemdas

        # iterate up tree to find value

    
    # if day is past max day for month, iterate month
    # if month is past max month for year, iterate year
    
    # cat values into m/d/y string
    return 


if __name__ == "__main__":
    try:
        print(parse_time(sys.argv[1]))
    except IndexError:
        print(parse_time("*+3/*/*"))