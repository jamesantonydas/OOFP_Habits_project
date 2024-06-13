from src.Habit import *
from math import ceil


def analytics_time_duration(recent_date: datetime, older_date: datetime, periodicity = HabitPeriods.DAILY) -> int:
    """ Calculates the distance between two dates, based on the periodicity. (daily, weekly, etc.)

    :param recent_date: the recent date, from today
    :param older_date: the older date, from today
    :param periodicity: the periodicity of the habit
    :return: the distance between the dates
    :rtype: int
    """
    if periodicity == HabitPeriods.DAILY:
        return (recent_date - older_date).days
    elif periodicity == HabitPeriods.WEEKLY:
        days_inbetween = (recent_date - older_date).days
        r = ((recent_date.weekday() + 1) % 7) + 1
        o = ((older_date.weekday() + 1) % 7) + 1
        return 0 if days_inbetween < 7 else ceil((days_inbetween - (r - 1) - (7 - o)) / 7)
    elif periodicity == HabitPeriods.MONTHLY:
        return (recent_date.year - older_date.year) * 12 + recent_date.month - older_date.month
    elif periodicity == HabitPeriods.YEARLY:
        return recent_date.year - older_date.year
    return 0


def analyze_streak(h_dates, older, periodicity) -> tuple[int, int]:
    """ Recursive function for calculating the streaks.

    :param h_dates: list of dates to calculate from.
    :param older: the older date from the previous iteration.
    :param periodicity: periodicity of the habit
    :return: returns current streak, and longest streak.
    :rtype: tuple[int, int]
    """
    if not h_dates:
        return 0, 0

    time_diff = analytics_time_duration(older, h_dates[-1], periodicity)

    # checking the end of list
    if (len(h_dates)) <= 1:
        return (2, 2) if time_diff == 1 else (0, 1)

    # calling the recursion
    current, longest = analyze_streak(h_dates[0:-1], h_dates[-1], periodicity)

    if time_diff == 1:
        return current + 1, max(current + 1, longest)
    elif time_diff < 0:
        return 0, 0
    else:
        return 1, longest


def analytics_habit_streak(h_dates: list, periodicity) -> tuple[int, int]:
    """ Function for wrapping analyze_streak function, finalizes the results.

    :param h_dates: list of dates from habit object
    :param periodicity: habit periodicity.
    :return: returns current streak, and longest streak.
    :rtype: tuple[int, int]
    """

    if not h_dates:
        return 0, 0

    current_streak, longest_streak = analyze_streak(h_dates[0:-1], h_dates[-1], periodicity)

    diff = analytics_time_duration(datetime.now(), h_dates[-1], periodicity)
    if diff > 2:
        return 0, longest_streak
    elif diff < 0:
        return 0, 0

    return current_streak, longest_streak


def analyze_breaks(h_dates, older, periodicity) -> tuple:
    """ Recursive function for calculates longest break, and total number of breaks.

    :param h_dates: list of dates.
    :param older: oldest date from the previous iteration.
    :param periodicity: periodicity of the habit
    :return: longest break, total number of breaks.
    :rtype: tuple[int, int]
    """
    if not h_dates:
        return 0, 0

    time_diff = analytics_time_duration(older, h_dates[-1], periodicity)

    # checking the end of list
    if (len(h_dates)) <= 1:
        return (time_diff - 1, 1) if time_diff > 1 else (0, 0)

    # calling the recursion
    longest, total = analyze_breaks(h_dates[0:-1], h_dates[-1], periodicity)
    if time_diff == 1:
        return longest, total
    elif time_diff < 0:
        return 0, 0
    else:
        return max(time_diff - 1, longest), total + 1


def analytics_habit_breaks(h_dates: list, periodicity) -> tuple[int, int]:
    """ Function acts as a wrapper to the analyze_breaks function. Finalizes the results.

    :param h_dates: list of dates from the habit object.
    :param periodicity: periodicity of the habit object.
    :return: longest breaks, total breaks.
    :rtype: tuple[int, int]
    """
    if not h_dates:
        return 0, 0

    longest_break, total_breaks = analyze_breaks(h_dates[0:-1], h_dates[-1], periodicity)

    diff = analytics_time_duration(datetime.now(), h_dates[-1], periodicity)
    if diff > 2:
        return max(diff - 1, longest_break), total_breaks + 1
    elif diff < 0:
        return 0, 0

    return longest_break, total_breaks


# Functions are implemented with recursion.
def list_currently_tracked_habits(habit_data: list) -> list:
    """Lists the names of currently tracked habits

    :param list habit_data: list of all habit objects
    :return: list of names as string
    """
    if not habit_data:
        return []
    else:
        habit = habit_data[0]
        result = [habit.name]
        return result + list_currently_tracked_habits(habit_data[1:])


def list_currently_unchecked_habits(habit_data: list) -> list:
    """Lists the names of currently unchecked habits for today

    :param list habit_data: list of all habit objects
    :return: list of names as string
    """
    if not habit_data:
        return []
    else:
        habit = habit_data[0]
        result = [habit.name] if habit.is_checked_off() is False else []
        return result + list_currently_unchecked_habits(habit_data[1:])


def list_currently_checked_habits(habit_data: list) -> list:
    """ Lists the names of currently checked habits for today

    :param list habit_data: list of all habit objects
    :return: list of names as string
    """
    if not habit_data:
        return []
    else:
        habit = habit_data[0]
        result = [habit.name] if habit.is_checked_off() is True else []
        return result + list_currently_checked_habits(habit_data[1:])


def list_habit_with_periodicity(habit_data: list, periodicity = HabitPeriods.DAILY):
    """ Lists the names of habit with given periodicity

    :param list habit_data: list of all habit objects.
    :param HabitPeriods periodicity: periodicity to be selected.
    :return: list of names as string
    """
    if not habit_data:
        return []
    else:
        habit = habit_data[0]
        result = [habit.name] if habit.periodicity == periodicity else []
        return result + list_habit_with_periodicity(habit_data[1:], periodicity)


def str_truncate(name: str) -> str:
    """ Truncate the given string for table

    :param name: string to be truncated.
    :return: resulting string
    """
    n_length = 30
    if len(name) > (n_length - 3):
        return name[:(n_length - 3)] + "..."
    else:
        return name + (" " * (n_length - len(name)))


def float_truncate(number: float) -> str:
    """ Truncate the given float for usage in tables

    :param number: number to be truncated
    :return: resulting number.
    """
    n_length = 4
    num = str(round(number))
    if len(num) > (n_length - 1):
        return num[:(n_length - 1)] + '.'
    else:
        return num + (' ' * (n_length - len(num)))


def habit_info(habit: Habit) -> str:
    """ Add analytic information to the given list of habit name

    :param Habit habit: Habit object to be generated
    :return: string containing analytical information
    :rtype: str
    """
    current_streak, longest_streak = habit.habit_streak()
    check_icon = "\N{White Heavy Check Mark}" if habit.is_checked_off() else "\N{White Square Button}"
    stats = ("" + check_icon + " " + str_truncate(habit.name) +
             "  \N{Fire} " + float_truncate(current_streak) +
             " \N{sunflower} " + float_truncate(longest_streak) +
             " \N{Stopwatch} " + habit.periodicity.value)
    return stats


def list_habit_info(habit_data: dict, name_list: list) -> list:
    """ Lists the analytics info of the given habit names

    :param Habit habit_data: list of all habit objects
    :param name_list: list of names of habit
    :return: list of analytics information
    :rtype: list
    """
    if not name_list:
        return []
    else:
        return [habit_info(habit_data[name_list[0]])] + list_habit_info(habit_data, name_list[1:])


def habit_analytics(habit: Habit) -> list:
    """ Creates a list of all analytical information of the given habit object,
    such as name, current streak, longest streak, longest breaks, total breaks, total checkoffs,
    total task duration, habit periodicity, habit creation date and habit description.

    :param Habit habit: habit object
    :return: list of analytical information
    :rtype: list
    """
    habit_table = []
    current_streak, longest_streak = habit.habit_streak()
    longest_break, total_breaks = habit.habit_breaks()
    total_checkoffs, total_duration = habit.habit_stats()

    habit_table.extend([
        habit.name,
        round(current_streak),
        round(longest_streak),
        round(longest_break),
        round(total_breaks),
        round(total_checkoffs),
        round(total_duration),
        habit.periodicity.value,
        habit.get_creation_date(),
        habit.description
    ])
    return habit_table


def list_habit_analytics(habit_data: dict, name_list: list):
    """ Generates a list containing list of analytical information of given habit names.

    :param dict habit_data: dictionary of habit objects
    :param name_list: list containing the name of the habits
    :return: list of habit names with analytics.
    """
    if not name_list:
        return []
    else:
        return [habit_analytics(habit_data[name_list[0]])] + list_habit_analytics(habit_data, name_list[1:])


def habit_analytics_table(habit: Habit) -> list:
    """ Creates a list of all analytical information of the given habit object,
    such as name, current streak, longest streak, longest breaks, total breaks, total checkoffs,
    total task duration, habit periodicity, habit creation date and habit description.

    :param Habit habit: habit object
    :return: list of analytical information
    :rtype: list
    """
    habit_info_table = []
    current_streak, longest_streak = habit.habit_streak()
    longest_break, total_breaks = habit.habit_breaks()
    total_checkoffs, total_duration = habit.habit_stats()

    habit_info_table.extend([
        habit.name,
        round(current_streak),
        round(longest_streak),
        round(longest_break),
        round(total_breaks),
        round(total_checkoffs),
        round(total_duration),

    ])
    return habit_info_table


def list_habit_analytics_table(habit_data: dict, name_list: list):
    """ Generates a list containing list of analytical information of given habit names.

    :param dict habit_data: dictionary of habit objects
    :param name_list: list containing the name of the habits
    :return: list of habit names with analytics.
    """
    if not name_list:
        return []
    else:
        return [habit_analytics_table(habit_data[name_list[0]])] + list_habit_analytics_table(habit_data, name_list[1:])
