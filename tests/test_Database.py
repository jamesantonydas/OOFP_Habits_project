import pytest
import os
from src.Database import *
from freezegun import freeze_time


@pytest.fixture(scope = "session")
def test_database():
    db_name = "test_database.db"
    initialize_database(db_name)
    yield db_name
    # deleting the database after testing
    os.remove(db_name)


@freeze_time("2024-05-30")
def test_add_habit(test_database):
    habit_obj1 = Habit('test1')
    habit_obj2 = Habit('test2')
    add_habit_to_db(test_database, habit_obj1)
    add_habit_to_db(test_database, habit_obj2)
    print("\n Testing add habit to database..")
    assert is_habit_exists(test_database, 'test1') is True
    assert is_habit_exists(test_database, 'test2') is True


def test_is_habit_exists(test_database):
    print("\n Testing is habit exists..")
    assert is_habit_exists(test_database, "test1") is True
    assert is_habit_exists(test_database, "test3") is False


def test_delete_habit(test_database):
    delete_habit(test_database, 'test1')
    print("\n Testing delete database")
    assert is_habit_exists(test_database, "test1") is False


def test_load_habit_data(test_database):
    habit_data = load_habit_data(test_database)
    print("\n Testing load database")
    assert len(habit_data) == 1
    assert habit_data[0][0] == 'test2'


@freeze_time("2024-05-30")
def test_load_habit_history(test_database):
    habit_obj = Habit('test1')
    habit_obj.check_off()
    add_habit_to_db(test_database, habit_obj)
    history_data = load_habit_history(test_database)
    print("\n Testing load history data..")
    assert len(history_data) == 2
    for history in history_data:
        if history[0] == "test1":
            assert history[1] == "2024-05-30"
        if history[0] == "test2":
            assert history[1] == ""


@freeze_time("2024-05-30")
def test_update_habit_data(test_database):
    habit_obj1 = Habit('test1', "test desc", periodicity = HabitPeriods.YEARLY)
    update_habit_data(test_database, habit_obj1)
    print("\n Testing update habit data..")
    habits = load_habit_data(test_database)
    for habit in habits:
        if habit[0] == 'test1':
            assert habit[2] == 'yearly'


@freeze_time("2024-05-30")
def test_update_habit_history(test_database):
    habit_obj1 = Habit('test1', "test desc", periodicity = HabitPeriods.YEARLY)
    habit_obj1.check_off()
    update_habit_data(test_database, habit_obj1)
    print("\n Testing update habit history..")
    habits = load_habit_history(test_database)
    for habit in habits:
        if habit[0] == 'test1':
            assert habit[1] == '2024-05-30'
