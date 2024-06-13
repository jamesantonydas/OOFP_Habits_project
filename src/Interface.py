import questionary as qt
from src.HabitManager import *
from tabulate import tabulate
from src.Analytics import habit_analytics


def ask_habit_name():
    """ CLI elements for asking habit name from user"""
    message = "Please enter the Habit name: "
    return input(message)


def ask_habit_desc():
    """ CLI elements for asking habit description from user"""
    message = "Describe the habit in a few words: "
    return input(message)


def ask_habit_periodicity():
    """ CLI elements for selecting habit periodicity"""
    message = "Please select the habit periodicity:"
    options = ['daily', 'weekly', 'monthly', 'yearly']
    return qt.select(message, choices = options).ask()


def edit_habit_desc(habit_name: str, habit_manager: HabitManager):
    """ CLI elements for editing habit description

    :param str habit_name: name of the habit to be edited
    :param HabitManager habit_manager: link form HabitTrackerCLI object.
    :returns: None
    """
    message = "\n Please enter the new Description: "
    new_desc = input(message)
    if (not new_desc.isalpha()) and (len(new_desc) < 1):
        print("\n Please enter a better description ")
        return
    habit_manager.edit_habit_description(habit_name, new_desc)
    return


def edit_habit_periodicity(habit_name: str, habit_manager: HabitManager):
    """ CLI elements for editing habit periodicity

    :param str habit_name: name of the habit to be edited
    :param HabitManager habit_manager: link form HabitTrackerCLI object.
    :returns: None
    """
    message = "Please enter the new Periodicity"
    options = ['daily', 'weekly', 'monthly', 'yearly']
    new_period = qt.select(message, choices = options).ask()
    print("\nChanging Habit periodicity will reset the task. You will lose your progress.")
    print("Do you want to change the periodicity to ", new_period)
    options = ['Yes', 'No']
    selection = qt.select(message, choices = options).ask()
    if selection == 'Yes':
        habit_manager.edit_habit_periodicity(habit_name, HabitPeriods(new_period))
    return


def rename_habit(habit_name: str, habit_manager: HabitManager):
    """ CLI elements for renaming the habit

    :param str habit_name: name of the habit to be edited
    :param HabitManager habit_manager: Link from HabitTrackerCLI object.
    :return: None
    """
    message = "Please enter the new name for the Habit:"
    new_name = input(message)
    if (not new_name.isalpha()) and (len(new_name) < 1):
        print("\n Please enter a better description ")
        return
    habit_manager.edit_habit_name(habit_name, new_name)
    return


def check_or_uncheck_habit(habit_name: str, habit_manager: HabitManager):
    """ Checks off the given habit for today, if not Checked off for today.
    Un-Check off the given habit for today, if already Checked off for today.

    :param habit_name: habit name to check/uncheck
    :param habit_manager: Link from HabitTrackerCLI object.
    :returns: None
    """
    if not habit_manager.is_habit_exist(habit_name):
        return
    if habit_manager.habits[habit_name].is_checked_off():
        message = "Do you want to un-check the habit for today?"
        options = ['Yes', 'No']
        selection = qt.select(message, choices = options).ask()
        if selection == 'Yes':
            habit_manager.uncheck_habit(habit_name)
    else:
        message = "Do you want to check the habit for today?"
        options = ['Yes', 'No']
        selection = qt.select(message, choices = options).ask()
        if selection == 'Yes':
            habit_manager.check_off_habits([habit_name])
    return


def reset_habit(habit_name: str, habit_manager: HabitManager):
    """ Resets the habit history

    :param str habit_name: name of the habit to reset.
    :param HabitManager habit_manager: Link form HabitTrackerCLI object
    :returns: None
    """
    message = "Do you want to reset the Habit's history? This can't be undone"
    options = ['Yes', 'No']
    selection = qt.select(message, choices = options).ask()
    if selection == 'No':
        return
    habit_manager.edit_habit_reset(habit_name)
    print("Habit reset successful!")
    return


def delete_habit(habit_name: str, habit_manager: HabitManager):
    """ Deletes the habit from HabitManager

    :param str habit_name: name of the habit to be deleted
    :param HabitManager habit_manager: Link from the HabitTrackerCLI object
    :returns: None
    """
    message = "Do you want to delete the habit?:" + habit_name
    menu = ['Yes', 'No']
    option = qt.select(message, choices = menu).ask()
    if option == 'No':
        return
    try:
        if habit_manager.delete_habit(habit_name) is True:
            print("Habit successfully deleted")
        else:
            print("Habit doesn't exist!")
    except Exception as e:
        print("Something went wrong!\n", e)
    return


def habit_report_one(habit_name: str, habit_manager: HabitManager):
    """ Implements CLI element for tabulating the analytical information

    :param str habit_name: name of the habit
    :param HabitManager habit_manager: Link from HabitTrackerCLI object
    :returns: None
    """
    headers = ["Name", "Current Streak", "Longest Streak", "Longest Break", "Total Breaks", "Total Checkoffs",
               "Total Duration", "Periodicity", "Creation date"]
    table_style = "mixed_grid"
    habit = habit_manager.habits[habit_name]
    analytics_data = habit_analytics(habit)
    history_data = [[x, y] for x, y in zip(headers, analytics_data)]
    print("\n Analytics for ", habit_name, "\n")
    print(tabulate(history_data, tablefmt = table_style))
    return
