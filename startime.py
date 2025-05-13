import sys
from simpleeval import simple_eval
from datetime import date as dtdate

# list of valid symbols, using any outside of this set will raise an error
math_symbols = '+-/*'
grouping_symbols = '()' # hardcoded for parentheses right now.


days_in_month = [0,31,28,31,30,31,30,31,31,30,31,30,31]

# returns whether the given year is a leap year
def is_leap_year(year: int) -> bool:
    return year%4 == 0 and (year%100 != 0 or year%400 == 0)
    
# given a day and year, how many days (int) are in the month?
def get_days_in_month(month: int, year: int) -> int:
    return days_in_month[month] + int(is_leap_year(year) and month == 2)

# make sure that values used aren't absurd
def sanity_check(val: str, inp: str) -> None:
    if "WILD" not in val and (not val.isnumeric() or abs(int(val)) > 100000): 
        raise ValueError(f"Operand {val} in date {inp} is malformed or unusually large.")

# given a startime string, split into tokens of numbers, symbols, and WILD elements (wildcard star)
def tokenize_startime(inp: str) -> list[str]:
    tokens = []

    # clean input
    inp = inp.replace("()","") # empty grouping symbols can mess up simple eval

    # turn input into tokens
    expression = []
    wildcard_pos = []
    last = ""
    grouping_depth = 0
    for char in inp:
        if char.isnumeric(): # number
            if last == "OPERATOR" or last == "GROUPING":
                last = ""
                if expression[-1] == ")": # implicit mult
                    expression.append("*")
            last += str(char)
        elif char in math_symbols: # operator
            if last and last != "OPERATOR" or last == "GROUPING":
                if last != "" and last != "GROUPING": 
                    sanity_check(last,inp)
                    expression.append(last)
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
            grouping_depth += 1 if char == "(" else -1
            if last and last != "OPERATOR" and last != "GROUPING":
                sanity_check(last,inp)
                expression.append(last)
                if char == "(": # implicit mult
                    expression.append("*")
            elif last == "GROUPING":
                if char == "(": # implicit mult
                    expression.append("*")
            expression.append(char)
            last = "GROUPING"
        else: # unknown, raise error
            raise ValueError(f"Unrecognized character '{char}' passed into date '{inp}'.")
    
    if last != "": # don't forget the last number if any
        expression.append(last)
    tokens.append(expression)

    if grouping_depth != 0: # missing or too many grouping symbols
        raise ValueError(f"Grouping mismatch in date {inp} are invalid.")
    
    if len(tokens) != 3: # missing or misplaced '/'s
        raise ValueError(f"Date {inp} is malformed.")
    
    return tokens

component_names = ["month","day","year"] # for more descriptive errors
def eval_tokenized_startime(tokens: list[str]) -> str:
    today = dtdate.today().strftime("%m/%d/%Y").split("/")
    date = [0,0,0]
    for i, token in enumerate(tokens): # get raw values
        exp = ''.join(token).replace("WILD",str(int(today[i])))
        try:
            val = simple_eval(exp)
        except ZeroDivisionError:
            raise ZeroDivisionError(f"Attempted to divide by zero when computing {component_names[i]} {exp}")
        date[i] = round(val)
    
    if date[0] > 12: # month-year wrapping
        date[2] += date[0]//12
        date[0] = (date[0]-1)%12+1

    cur_days = get_days_in_month(date[0],date[2])
    while date[1] > cur_days: # day-month wrapping
        date[1] -= cur_days
        date[0] += 1
        if date[0] > 12:
            date[2] += 1
            date[0] -= 12
        cur_days = get_days_in_month(date[0],date[2])

    # TODO: implement
    while date[1] < cur_days: # day-month wrapping backwards
        date[0] = date[0]
        #date[1] +
        break

    for i, val in enumerate(date):
        s_val = str(val)
        if len(s_val) == 1: # make sure months and days have leading 0 if 1 digit
            s_val = "0"+s_val
        
        date[i] = s_val
    
    return date

def parse_time(inp: str) -> str:
    tokens = tokenize_startime(inp)
    result = eval_tokenized_startime(tokens)
    return '/'.join(result)

if __name__ == "__main__":
    try:
        print(parse_time(sys.argv[1]))
    except IndexError: # nothing provided, assume today?
        print(parse_time("*/*/*")) # today
        parse_time("*/*+(5)(3*(2+3))/*")