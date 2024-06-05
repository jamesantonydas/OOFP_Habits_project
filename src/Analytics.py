from src.Habit import *


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


def list_habit_with_periodicity(habit_data: list, periodicity=HabitPeriods.DAILY):
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
        return name + (" "*(n_length - len(name)))


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
        return num + (' '*(n_length - len(num)))


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
