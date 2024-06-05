import sqlite3
import contextlib as clib
from src.Habit import *


def initialize_database(db_name: str):
    """ Initializes the database by creating if tables doesn't exist

    :param str db_name: Name of the database
    :return: Returns True if successfully initialized.
    """

    query1 = """CREATE TABLE IF NOT EXISTS HabitData (
    habit_name TEXT PRIMARY KEY ,
    descr TEXT,
    periodicity TEXT,
    creation_date TEXT
    )"""

    query2 = """CREATE TABLE IF NOT EXISTS HabitHistory (
    habit_name TEXT,
    history TEXT
    )"""

    with clib.closing(sqlite3.connect(db_name)) as con:
        with con:
            with clib.closing(con.cursor()) as cursor:
                cursor.execute(query1)
                cursor.execute(query2)
                con.commit()
    return True


def add_habit_to_db(db_name: str, habit: Habit):
    """ Adds habit to the database

    :param str db_name: Name of the database file
    :param Habit habit: Habit object to be added to the database
    :return: True if successfully added, False otherwise
    :rtype: bool
    """

    with clib.closing(sqlite3.connect(db_name)) as con:
        with con:
            with clib.closing(con.cursor()) as cursor:
                cursor.execute("INSERT INTO HabitData VALUES(?, ?, ?, ?)",
                               (habit.name, habit.description, habit.periodicity.value, habit.get_creation_date()))
                cursor.execute("INSERT INTO HabitHistory VALUES(?,?)",
                               (habit.name, habit.get_history()))
                con.commit()
    return True


def is_habit_exists(db_name, name: str) -> bool:
    """ Checks if the given habit name is present in the database

    :param str db_name: Name of the database file
    :param str name: Name of the Habit to check
    :return: True if the habit present in the database, False otherwise
    :rtype: bool
    """

    with clib.closing(sqlite3.connect(db_name)) as con:
        with con:
            with clib.closing(con.cursor()) as cursor:
                cursor.execute("SELECT * FROM HabitData WHERE habit_name == ?", (name,))
                sample_data = cursor.fetchone()
                return True if sample_data is not None else False


def delete_habit(db_name: str, name: str) -> None:
    """ Delete the given habit from the database

    :param str db_name: Name of the database file
    :param str name: Name of the habit to delete
    :return: Returns True if the habit is successfully deleted, False otherwise
    """

    with clib.closing(sqlite3.connect(db_name)) as con:
        with con:
            with clib.closing(con.cursor()) as cursor:
                cursor.execute("DELETE FROM HabitData WHERE habit_name == ?", (name,))
                cursor.execute("DELETE FROM HabitHistory WHERE habit_name == ?", (name,))
                con.commit()
    return


def load_habit_data(db_name: str) -> list:
    """ Loads the data from the given database

    :param str db_name: Name of the database file
    :return: list of sql row objects
    :rtype: list
    """

    with clib.closing(sqlite3.connect(db_name)) as con:
        with con:
            con.row_factory = sqlite3.Row
            with clib.closing(con.cursor()) as cursor:
                cursor.execute("SELECT * FROM HabitData")
                result = [row for row in cursor.fetchall()]
                return result


def load_habit_history(db_name: str) -> list:
    """ Loads habit history from the given database

    :param str db_name : The name of the given database file
    :return: a list of sql row objects
    :rtype: list
    """

    with clib.closing(sqlite3.connect(db_name)) as con:
        with con:
            con.row_factory = sqlite3.Row
            with clib.closing(con.cursor()) as cursor:
                cursor.execute("SELECT * FROM HabitHistory")
                result = [row for row in cursor.fetchall()]
                return result


def update_habit_data(db_name, habit: Habit):
    """ Updates the habit data from the given object

    :param str db_name: Name of the given database file
    :param Habit habit: Habit object to be updated
    :return: True if successfully updated else false
    :rtype: bool
    """

    with clib.closing(sqlite3.connect(db_name)) as con:
        with con:
            con.row_factory = sqlite3.Row
            with clib.closing(con.cursor()) as cursor:
                cursor.execute(
                    "UPDATE HabitData SET descr = ?, periodicity = ?, creation_date = ? WHERE habit_name == ?",
                    (habit.description, habit.periodicity.value, habit.get_creation_date(), habit.name))
    return


def update_habit_history(db_name, habit: Habit):
    """ Updates the habit history data from the given Habit object

    :param str db_name: Name of the given database file
    :param Habit habit: Habit object to be updated
    :return: True if successfully updated, else returns false
    :rtype: bool
    """

    with clib.closing(sqlite3.connect(db_name)) as con:
        with con:
            con.row_factory = sqlite3.Row
            with clib.closing(con.cursor()) as cursor:
                cursor.execute("UPDATE HabitHistory SET history = ? WHERE habit_name == ?",
                               (habit.get_history(), habit.name,))
    return
