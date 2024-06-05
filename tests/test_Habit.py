import pytest
from freezegun import freeze_time
from src.Habit import *

data_streak = [["2024-05-27,2024-05-28,2024-05-29,2024-05-30", 4, 4],
               ["2024-05-26,2024-05-28,2024-05-29,2024-05-30", 3, 3],
               ["2024-05-25,2024-05-26,2024-05-27,2024-05-28", 0, 4],
               ["2024-05-24,2024-05-25,2024-05-26,2024-05-30", 1, 3],
               ["", 0, 0]]


@freeze_time("2024-05-30")
@pytest.mark.parametrize(('history', 'current_streak', 'longest_streak'), data_streak)
def test_habit_streak(history: str, current_streak: float, longest_streak: float):
    """ Tests habit streaks from Habit class"""
    habit_obj = Habit("test", "test",
                      HabitPeriods.DAILY, "2024-05-15", history)
    current, longest = habit_obj.habit_streak()
    print('\nCalculated streak: current', current, "longest:", longest)
    assert current == current_streak
    assert longest == longest_streak


streak_weekly = [["2024-05-8,2024-05-15,2024-05-22,2024-05-29", 4, 4],
                 ["2024-04-26,2024-05-15,2024-05-22,2024-05-29", 3, 3],
                 ["2024-04-1,2024-05-8,2024-05-21,2024-05-28", 2, 2],
                 ["2024-05-3,2024-05-10,2024-05-17,2024-05-29", 1, 3],
                 ["", 0, 0]]


@freeze_time("2024-05-30")
@pytest.mark.parametrize(('history', 'current_streak', 'longest_streak'), streak_weekly)
def test_habit_streak_weekly(history: str, current_streak: float, longest_streak: float):
    """ Tests habit streaks from Habit class"""
    habit_obj = Habit("test", "test",
                      HabitPeriods.WEEKLY, "2023-05-15", history)
    current, longest = habit_obj.habit_streak()
    print('\nCalculated weekly streak: current', current, "longest:", longest)
    assert current == current_streak
    assert longest == longest_streak


streak_monthly = [["2024-02-27,2024-03-28,2024-04-29,2024-05-30", 4, 4],
                  ["2024-01-26,2024-03-28,2024-04-29,2024-05-30", 3, 3],
                  ["2023-12-25,2024-01-26,2024-02-27,2024-05-28", 1, 3],
                  ["2023-12-24,2024-02-25,2024-04-26,2024-05-30", 2, 2],
                  ["", 0, 0]]


@freeze_time("2024-05-30")
@pytest.mark.parametrize(('history', 'current_streak', 'longest_streak'), streak_monthly)
def test_habit_streak_monthly(history: str, current_streak: float, longest_streak: float):
    """ Tests habit streaks from Habit class"""
    habit_obj = Habit("test", "test",
                      HabitPeriods.MONTHLY, "2024-05-15", history)
    current, longest = habit_obj.habit_streak()
    print('\nCalculated monthly streak: current', current, "longest:", longest)
    assert current == current_streak
    assert longest == longest_streak


streak_yearly = [["2021-05-27,2022-05-28,2023-05-29,2024-05-30", 4, 4],
                 ["2019-05-25,2020-05-28,2021-05-29,2022-04-28", 0, 4],
                 ["2020-05-25,2021-05-26,2022-05-27,2024-05-28", 1, 3],
                 ["2019-05-24,2020-05-25,2021-05-28,2023-05-29", 1, 3],
                 ["", 0, 0]]


@freeze_time("2024-05-30")
@pytest.mark.parametrize(('history', 'current_streak', 'longest_streak'), streak_yearly)
def test_habit_streak_yearly(history: str, current_streak: float, longest_streak: float):
    """ Tests habit streaks from Habit class"""
    habit_obj = Habit("test", "test",
                      HabitPeriods.YEARLY, "2015-05-15", history)
    current, longest = habit_obj.habit_streak()
    print('\nCalculated yearly streak: current', current, "longest:", longest)
    assert current == current_streak
    assert longest == longest_streak


data_breaks = [["2024-05-20,2024-05-28,2024-05-29,2024-05-30", 7, 1],
               ["2024-05-25,2024-05-27,2024-05-29,2024-05-30", 1, 2],
               ["2024-05-23,2024-05-24,2024-05-28,2024-05-30", 3, 2],
               ["2024-05-23,2024-05-24,2024-05-25,2024-05-26", 3, 1],
               ["2024-05-23,2024-05-24,2024-05-25,2024-05-29", 3, 1],
               ["", 0, 0]]


@freeze_time("2024-05-30")
@pytest.mark.parametrize(('history', 'longest_break', 'total_breaks'), data_breaks)
def test_habit_breaks(history: str, longest_break: float, total_breaks: float):
    """ Tests habit breaks from Habit class"""
    habit_obj = Habit("test", "test",
                      HabitPeriods.DAILY, "2024-05-15", history)
    longest, total = habit_obj.habit_breaks()
    print('\nCalculated breaks: longest:', longest, "total:", total)
    assert longest == longest_break
    assert total == total_breaks


data_stats = [["2024-05-27,2024-05-28,2024-05-29,2024-05-30", 4, 4],
              ["2024-05-28,2024-05-29,2024-05-30", 3, 4],
              ["2024-05-27,2024-05-28", 2, 4],
              ["2024-05-28", 1, 4]]


@freeze_time("2024-05-30")
@pytest.mark.parametrize(('history', 'total_checkoff', 'total_duration'), data_stats)
def test_habit_stats(history: str, total_checkoff: float, total_duration: float):
    """ Tests habit stats from Habit class"""
    habit_obj = Habit("test", "test",
                      HabitPeriods.DAILY, "2024-05-27", history)
    checkoff, duration = habit_obj.habit_stats()
    print("\nCalculated stats: total checkoff:", checkoff, "total duration:", duration)
    assert total_checkoff == checkoff
    assert total_duration == duration


@freeze_time("2024-05-30")
def test_get_history():
    """ Testing the get history from Habit class"""
    print("\n get history test 1 with datetime..")
    history = "2024-05-25,2024-05-26,2024-05-27,2024-05-30"
    habit_obj = Habit("test", "test",
                      HabitPeriods.DAILY, "2024-05-27", history)
    assert habit_obj.get_history() == history
    print("\n get history test 2 without datetime..")
    habit_obj = Habit("test")
    assert habit_obj.get_history() == ""


@freeze_time("2024-05-30")
def test_check_off():
    """ Testing the check off from Habit class"""
    history1 = "2024-05-25,2024-05-26,2024-05-27"
    history2 = "2024-05-25,2024-05-26,2024-05-27,2024-05-30"
    habit_obj = Habit("test", "test",
                      HabitPeriods.DAILY, "2024-05-27", history1)
    assert habit_obj.get_history() == history1
    print("\nTesting check off from habit object")
    habit_obj.check_off()
    assert habit_obj.get_history() == history2


@freeze_time("2024-05-30")
def test_is_checked_off():
    """ Testing is checked off from Habit Class """
    history = "2024-05-25,2024-05-26,2024-05-27,2024-05-28"
    habit_obj = Habit("test", "test",
                      HabitPeriods.DAILY, "2024-05-27", history)
    print("\nTesting if habit is checked off..")
    assert habit_obj.is_checked_off() is False
    print("\nChecking off habit..")
    habit_obj.check_off()
    print("\nTesting if habit is checked off..")
    assert habit_obj.is_checked_off() is True


@freeze_time("2024-05-30")
def test_uncheck_habit():
    """ Testing uncheck from Habit class """
    history = "2024-05-25,2024-05-26,2024-05-27,2024-05-30"
    history2 = "2024-05-25,2024-05-26,2024-05-27"
    habit_obj = Habit("test", "test",
                      HabitPeriods.DAILY, "2024-05-27", history)
    print("\n Testing if habit is checked off..")
    assert history == habit_obj.get_history()
    print("\n Un-checking off habit..")
    habit_obj.uncheck_habit()
    print("\n testing if habit is unchecked off")
    assert history2 == habit_obj.get_history()


@freeze_time("2024-05-30")
def test_get_creation_date():
    """ Testing get creation date from Habit class"""
    history = "2024-05-25,2024-05-26,2024-05-27,2024-05-30"
    habit_obj = Habit("test", "test",
                      HabitPeriods.DAILY, "2024-05-27", history)
    print("\n Testing creation date with parameter..")
    assert habit_obj.get_creation_date() == "2024-05-27"
    habit_obj2 = Habit('test')
    print("\n Testing creation date without parameter..")
    assert habit_obj2.get_creation_date() == "2024-05-30"
