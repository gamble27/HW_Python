from datetime import datetime as dt


def date_belongs_to_interval(date, start, end):
    # [0] - day
    # [1] - mon
    # [2] - year
    if ((dt(*date[::-1]) >= dt(*start[::-1]))
            and (dt(*date[::-1]) <= dt(*end[::-1]))):
        return True
    return False


def date_is_less_than_start(date, start):
    # [0] - day
    # [1] - mon
    # [2] - year
    if dt(*date[::-1]) < dt(*start[::-1]):
        return True
    return False

# def date_is_greater_than_end(date, end):
#     # [0] - day
#     # [1] - mon
#     # [2] - year
#     if (dt(*date[::-1]) > dt(*end[::-1])):
#         return True
#     return False


class ParserError(BaseException):
    pass
