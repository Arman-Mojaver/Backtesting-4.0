from utils.date_utils import string_to_datetime


def get_difference_in_years(date_1: str, date_2: str) -> float:
    datetime_1, datetime_2 = string_to_datetime(date_1), string_to_datetime(date_2)

    # Using 365.25 to account for leap years
    return round(abs((datetime_1 - datetime_2).days) / 365.25, 2)
