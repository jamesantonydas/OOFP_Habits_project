import datetime
from random import randint
from datetime import timedelta
from dateutil.relativedelta import relativedelta


def generate_data(dates: list) -> tuple:
    """ Simulates user activity by selecting random dates from the given list of dates.
        High probability of task completion.

    :param dates: list of dates to select from.
    :return: list of dates, current streak, longest steak, longest break, total breaks
    """

    selected_dates = []
    current_streak = 0
    current_break = 0
    longest_streak = 0
    longest_break = 0
    total_breaks = 0

    for date in dates[:-1]:
        rand_num = randint(0, 100)
        rand = 0 if rand_num < 25 else 1

        if rand == 1:
            selected_dates.append(date)
            current_streak += 1
            current_break = 0
            longest_streak = max(current_streak, longest_streak)

        if rand == 0:
            current_streak = 0
            current_break += 1
            longest_break = max(longest_break, current_break)
            total_breaks += 1

    rand_last = randint(0, 100)
    rand = 0 if rand_last < 25 else 1

    if rand == 1:
        selected_dates.append(dates[-1])
        current_streak += 1
        longest_streak = max(current_streak, longest_streak)

    history = []
    for dt in selected_dates:
        history.append(dt.strftime('%Y-%m-%d'))
    final_dates = ','.join(history)

    return final_dates, current_streak, longest_streak, longest_break, total_breaks


def generate_daily_test_data(start: datetime, end: datetime) -> tuple:
    """ Function for generating daily test data

    :param start: date to start from
    :param end: date to end
    :return: dates as string, current streak, longest streak, longest breaks, total breaks
    :rtype: tuple[str, int, int, int]
    """
    days = (end - start).days
    dates = [start + timedelta(days = x) for x in range(days + 1)]
    return generate_data(dates)


def generate_weekly_test_data(start, end) -> tuple:
    """ Function for generating weekly test data

    :param start: date to start from
    :param end: date to end
    :return: dates as string, current streak, longest streak, longest breaks, total breaks
    :rtype: tuple[str, int, int, int]
    """
    days_inbetween = (end - start).days
    r = ((end.weekday() + 1) % 7) + 1
    o = ((start.weekday() + 1) % 7) + 1
    diff = 0 if days_inbetween < 7 else round((days_inbetween - (r - 1) - (7 - o)) / 7)
    dates = [start + timedelta(days = 7 * x) for x in range(diff + 1)]
    return generate_data(dates)


def generate_monthly_test_data(start, end) -> tuple:
    """ Function for generating monthly test data.

    :param start: date to start from
    :param end: date to end
    :return: dates as string, current streak, longest streak, longest breaks, total breaks
    :rtype: tuple[str, int, int, int]
    """
    diff = (end.year - start.year) * 12 + end.month - start.month
    dates = [start + relativedelta(months = x) for x in range(diff + 1)]
    return generate_data(dates)


def generate_yearly_test_data(start, end) -> tuple:
    """ Function for generating yearly test data

    :param start: date to start from
    :param end: date to end
    :return: dates as string, current streak, longest streak, longest breaks, total breaks
    :rtype: tuple[str, int, int, int]
    """
    diff = end.year - start.year
    dates = [start + relativedelta(years = x) for x in range(diff + 1)]
    return generate_data(dates)


def generate_test_data(start, end, periodicity = 'daily') -> tuple:
    """ Function for selecting appropriate functions

    :param start: date to start from
    :param end: date to end
    :param periodicity: periodicity
    :return: dates as string, current streak, longest streak, longest breaks, total breaks
    :rtype: tuple[str, int, int, int]
    """
    periods = {
        'daily': generate_daily_test_data,
        'weekly': generate_weekly_test_data,
        'monthly': generate_monthly_test_data,
        'yearly': generate_yearly_test_data
    }
    func = periods[periodicity]
    return func(start, end)
