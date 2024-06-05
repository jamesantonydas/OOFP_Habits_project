import pytest
from freezegun import freeze_time
from src.Analytics import *


@freeze_time("2024-05-30")
@pytest.fixture(scope = 'session')
def habit_list():
    a = Habit('test1', " test...", periodicity = HabitPeriods.DAILY, creation_date = "2024-05-15")
    b = Habit('test2', " test...", periodicity = HabitPeriods.DAILY, creation_date = "2024-05-15")
    c = Habit('test3', " test...", periodicity = HabitPeriods.WEEKLY, creation_date = "2024-05-15")
    d = Habit('test4', " test...", periodicity = HabitPeriods.WEEKLY, creation_date = "2024-05-15")
    e = Habit('test5', " test...", periodicity = HabitPeriods.MONTHLY, creation_date = "2024-05-15")
    f = Habit('test6', " test...", periodicity = HabitPeriods.MONTHLY, creation_date = "2024-05-15")
    g = Habit('test7', " test...", periodicity = HabitPeriods.YEARLY, creation_date = "2024-05-15")
    h = Habit('test8', " test...", periodicity = HabitPeriods.YEARLY, creation_date = "2024-05-15")

    return {'test1': a, 'test2': b, 'test3': c, 'test4': d,
            'test5': e, 'test6': f, 'test7': g, 'test8': h}


def test_currently_tracked_habits(habit_list):
    habits = list_currently_tracked_habits(list(habit_list.values()))
    print("\n testing currently tracked habits")
    assert habits == ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8']


@freeze_time("2024-05-30")
def test_checked_habits(habit_list):
    habit_list['test1'].check_off()
    habit_list['test3'].check_off()
    habit_list['test5'].check_off()
    habit_list['test6'].check_off()
    habits = list_currently_checked_habits(list(habit_list.values()))
    print("\n testing currently checked habits")
    assert habits == ['test1', 'test3', 'test5', 'test6']


@freeze_time("2024-05-30")
def test_unchecked_habits(habit_list):
    habits = list_currently_unchecked_habits(list(habit_list.values()))
    print("\n testing currently unchecked habits")
    assert habits == ['test2', 'test4', 'test7', 'test8']


def test_habits_with_periodicity_daily(habit_list):
    habits = list_habit_with_periodicity(list(habit_list.values()), periodicity = HabitPeriods.DAILY)
    print("\n Testing daily habits")
    assert habits == ['test1', 'test2']


def test_habits_with_periodicity_weekly(habit_list):
    habits = list_habit_with_periodicity(list(habit_list.values()), periodicity = HabitPeriods.WEEKLY)
    print("\n Testing weekly habits")
    assert habits == ['test3', 'test4']


def test_habits_with_periodicity_monthly(habit_list):
    habits = list_habit_with_periodicity(list(habit_list.values()), periodicity = HabitPeriods.MONTHLY)
    print("\n Testing monthly habits")
    assert habits == ['test5', 'test6']


def test_habits_with_periodicity_yearly(habit_list):
    habits = list_habit_with_periodicity(list(habit_list.values()), periodicity = HabitPeriods.YEARLY)
    print("\n Testing yearly habits")
    assert habits == ['test7', 'test8']
