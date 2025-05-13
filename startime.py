import sys
from ast import parse as ast_parse
from datetime import date

def add(a: int, b: int) -> int:
    return a+b
def sub(a: int, b: int) -> int:
    return a-b
def mult(a: int, b: int) -> int:
    return round(a*b)
def div(a: int, b: int) -> int:
    return round(a/b)


def is_leap_year(year: int) -> bool:
    return year%4 == 0 and (year%100 != 0 or year%400 == 0)
    
def get_days_in_month(month: int, year: int) -> bool:
    return days_in_month[month] + int(is_leap_year(year) and month == 2)

math_symbols = {'+': add, '-': sub, '*': mult, '/': div}
days_in_month = [0,31,28,31,30,31,30,31,31,30,31,30,31]

def tokenize_startime(inp: str) -> list[str]:
    tokens = []

    expression = []
    wildcard_pos = []
    last = ""
    grouping_depth = 0
    for char in inp:
        if char.isnumeric(): # number
            if last == "OPERATOR" or last == "GROUPING":
                last = ""
            last += str(char)
        elif char in math_symbols: # operator
            if last and last != "OPERATOR" or last == "GROUPING":
                if last != "" and last != "GROUPING": expression.append(last)
                if char == "/" and grouping_depth == 0:
                    tokens.append(expression)
                    last = ""
                    expression = []
                else:
                    expression.append(char)
                    last = "OPERATOR"
            elif char == "*":
                last = "WILD"
        elif char in "()": # grouping symbol
            if char == "(":
                grouping_depth += 1
            else:
                grouping_depth -= 1
            if last != "OPERATOR":
                expression.append(last)
            expression.append(char)
            last = "GROUPING"
        else: # unknown
            raise ValueError(f"Unknown value '{char}' passed into date '{inp}'.")
        print(char,expression)
    if last != "": 
        expression.append(last)
    tokens.append(expression)

    if grouping_depth != 0: # missing or too many grouping symbols
        raise ValueError(f"Grouping symbol(s) in date {inp} are invalid.")
    
    if len(tokens) != 3: # missing or misplaced '/'s
        raise ValueError(f"Date {inp} is malformed, are you grouping division?")
    return tokens

def eval_tree_exp(exp: str) -> int:
    print(exp)
    ast_parse(exp)


def parse_time(inp: str) -> str:
    # get dates
    today = date.today().strftime("%m/%d/%y").split("/")
    
    print(tokenize_startime(inp))

    #eval_tree_exp(split_input[i])

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
        print(parse_time("*+3*(3+3/5)-12/*/*"))