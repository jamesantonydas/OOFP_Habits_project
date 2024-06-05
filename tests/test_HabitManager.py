import pytest
import os
from src.HabitManager import *
from src.Analytics import *
from freezegun import freeze_time


@pytest.fixture(scope = "session")
def db_habit():
    db_name = "test_habit_manager.db"
    initialize_database(db_name)
    h1 = Habit('test1', "test..", periodicity = HabitPeriods.DAILY)
    h2 = Habit('test2', "test..", periodicity = HabitPeriods.WEEKLY)
    h3 = Habit('test3', "test..", periodicity = HabitPeriods.MONTHLY)
    add_habit_to_db(db_name, h1)
    add_habit_to_db(db_name, h2)
    add_habit_to_db(db_name, h3)
    yield db_name
    # delete habit manager db
    os.remove(db_name)


@freeze_time("2024-05-30")
def test_load_habits_from_db(db_habit):
    habit_manager = HabitManager(db_habit)
    print("\n Testing Load habits from db")
    assert len(habit_manager.habits) == 0
    habit_manager.load_habits_from_db()
    assert len(habit_manager.habits) == 3


def test_is_habit_exist(db_habit):
    habit_manager = HabitManager(db_habit)
    habit_manager.load_habits_from_db()
    print("\n Testing is habit exists")
    assert habit_manager.is_habit_exist('test1') is True
    assert habit_manager.is_habit_exist('test5') is False


@freeze_time("2024-05-30")
def test_add_habit_obj(db_habit):
    habit_manager = HabitManager(db_habit)
    habit_manager.load_habits_from_db()
    habit_manager.add_habit("test4", "test desc", HabitPeriods.MONTHLY)
    habit_list = habit_manager.data_as_dict()
    assert "test4" in list_currently_tracked_habits(list(habit_list.values()))


def test_delete_habit(db_habit):
    habit_manager = HabitManager(db_habit)
    habit_manager.load_habits_from_db()
    habit_manager.delete_habit('test4')
    habit_list = habit_manager.data_as_dict()
    assert "test4" not in list_currently_tracked_habits(list(habit_list.values()))


def test_edit_habit_name(db_habit):
    habit_manager = HabitManager(db_habit)
    habit_manager.load_habits_from_db()
    habit_manager.edit_habit_name('test3', 'test3_edited')
    habit_list = habit_manager.data_as_dict()
    current_habits = list_currently_tracked_habits(list(habit_list.values()))
    print("\n DEBUG: ", current_habits)
    assert "test3_edited" in current_habits
    assert "test3" not in current_habits


def test_edit_habit_periodicity(db_habit):
    habit_manager = HabitManager(db_habit)
    habit_manager.load_habits_from_db()
    assert habit_manager.habits['test1'].periodicity == HabitPeriods.DAILY
    habit_manager.edit_habit_periodicity('test1', HabitPeriods.YEARLY)
    assert habit_manager.habits['test1'].periodicity == HabitPeriods.YEARLY


def test_edit_habit_desc(db_habit):
    habit_manager = HabitManager(db_habit)
    habit_manager.load_habits_from_db()
    assert habit_manager.habits['test1'].description == 'test..'
    habit_manager.edit_habit_description('test1', 'testy')
    assert habit_manager.habits['test1'].description == 'testy'


@freeze_time("2024-05-30")
def test_check_off_habits(db_habit):
    habit_manager = HabitManager(db_habit)
    habit_manager.load_habits_from_db()
    habit_manager.check_off_habits(['test1', 'test2', 'test3_edited'])
    habit_list = habit_manager.data_as_dict()
    current_habits = list_currently_checked_habits(list(habit_list.values()))
    for habit_name in current_habits:
        assert habit_name in ['test1', 'test2', 'test3_edited']


@freeze_time("2024-05-30")
def test_uncheck_habit(db_habit):
    habit_manager = HabitManager(db_habit)
    habit_manager.load_habits_from_db()
    habit_manager.uncheck_habit('test3_edited')
    habit_list = habit_manager.data_as_dict()
    current_habits = list_currently_checked_habits(list(habit_list.values()))
    assert 'test1' in current_habits
    assert 'test2' in current_habits
    assert 'test3_edited' not in current_habits


def test_reset_habit(db_habit):
    habit_manager = HabitManager(db_habit)
    habit_manager.load_habits_from_db()
    assert habit_manager.habits['test1'].get_history() == "2024-05-30"
    habit_manager.edit_habit_reset('test1')
    assert habit_manager.habits['test1'].get_history() == ""
