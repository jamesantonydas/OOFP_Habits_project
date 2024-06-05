from src.Database import *
from src.SampleData import sample_habits


class HabitManager:

    def __init__(self, db_name: str = 'habit_data.db') -> None:
        """ Initializes the database connection for habit manager class

        :param str db_name: the name of the database file
        """
        self.habits = {}
        self.db_name = db_name
        initialize_database(db_name = db_name)
        return

    def add_habit_obj(self, habit: Habit) -> bool:
        """ Adds the habit object to the Habit manager

        :param Habit habit: the habit object to be added.
        :return: True if successfully added, false otherwise:
        :rtype: bool
        """
        if self.is_habit_exist(habit.name):
            return False
        self.habits[habit.name] = habit
        add_habit_to_db(self.db_name, habit)
        return True

    def load_habits_from_db(self) -> None:
        """ Loads Habit data from the database files to the habit classes

        :return: the function returns nothing
        """
        self.habits = {}
        data_list = load_habit_data(self.db_name)
        for data in data_list:
            habit = Habit(data[0], data[1], HabitPeriods(data[2]), data[3])
            self.habits[data[0]] = habit

        history_list = load_habit_history(self.db_name)
        for name, history in history_list:
            if name in self.habits:
                self.habits[name].set_history(history)

        if len(self.habits) < 1:
            sample_list = sample_habits()
            for sample in sample_list:
                self.add_habit_obj(sample)
        return

    def is_habit_exist(self, name: str) -> bool:
        """ Checks weather if the given habit name exists

        :param str name: habit name
        :return: True if habit name exists, false otherwise
        :rtype: bool
        """
        if name not in self.habits:
            return False
        if not is_habit_exists(self.db_name, name):
            return False
        return True

    def add_habit(self, name: str, desc: str = "",
                  periodicity: HabitPeriods = HabitPeriods.DAILY, history: str = "") -> bool:
        """ Adds habit name to the habit manager

        :param str name:
        :param str desc:
        :param HabitPeriods periodicity:
        :param str history:
        :return: True if successfully added, False otherwise.
        :rtype: bool
        """
        if self.is_habit_exist(name):
            return False
        habit_obj = Habit(name, desc, periodicity)
        if history != "":
            habit_obj.set_history(history)
        self.habits[name] = habit_obj
        add_habit_to_db(self.db_name, habit_obj)
        return True

    def delete_habit(self, name: str) -> bool:
        """ Deletes the habit from the application

        :param str name: habit name to be deleted
        :return: True if successfully deleted, False otherwise.
        :rtype: bool
        """
        if not self.is_habit_exist(name):
            return False
        delete_habit(self.db_name, name)
        del self.habits[name]
        return True

    def edit_habit_name(self, old_name: str, new_name: str) -> bool:
        """ Changes the name of the habit

        :param old_name: old name of the habit
        :param new_name: new name of the habit
        :return: True if changed successfully, False otherwise
        :rtype: bool
        """
        if not self.is_habit_exist(old_name):
            return False
        if self.is_habit_exist(new_name):
            return False
        old = self.habits[old_name]
        new_habit_obj = Habit(new_name, old.description, old.periodicity,
                              old.get_creation_date(), old.get_history())
        self.habits[new_name] = new_habit_obj
        del self.habits[old_name]
        delete_habit(self.db_name, old_name)
        add_habit_to_db(self.db_name, new_habit_obj)
        return True

    def edit_habit_description(self, name: str, desc: str) -> bool:
        """ Changes the description of the habit

        :param name: name of the habit
        :param desc: new description of the habit
        :return: True if changed successfully, False otherwise.
        :rtype: bool
        """
        if not self.is_habit_exist(name):
            return False
        habit_obj = self.habits[name]
        habit_obj.description = desc
        update_habit_data(self.db_name, habit_obj)
        return True

    def edit_habit_periodicity(self, name, periodicity):
        """ Changes the periodicity of the habit.
        Changing the periodicity will reset the history of the habit.

        :param name: name of the habit
        :param periodicity: new periodicity of the habit
        :return: True if successfully changed, False otherwise.
        """
        if not self.is_habit_exist(name):
            return False
        habit_obj = self.habits[name]
        habit_obj.periodicity = periodicity
        habit_obj.habit_history = []
        update_habit_data(self.db_name, habit_obj)
        return True

    def edit_habit_reset(self, name) -> bool:
        """ Resets the history of the habit

        :param str name: name of the habit
        :return: returns True if the reset is successful. False otherwise.
        :rtype: bool
        """
        if not self.is_habit_exist(name):
            return False
        habit_obj = self.habits[name]
        habit_obj.habit_history = []
        update_habit_history(self.db_name, habit_obj)
        return True

    def check_off_habits(self, habit_list: list) -> bool:
        """ Checks off the list of habits for today

        :param list habit_list: list of habit names to be checked off
        :return: True if successfully changed.
        """
        if not habit_list:
            return False
        for habit_name in habit_list:
            if self.is_habit_exist(habit_name):
                habit_obj = self.habits[habit_name]
                habit_obj.check_off()
                update_habit_history(self.db_name, habit_obj)
        return True

    def uncheck_habit(self, name: str):
        """ Unchecks the given habit for today

        :param str name: name of the habit
        :return: True if the habit is successfully unchecked. False otherwise.
        :rtype: bool
        """
        if name not in self.habits:
            return False
        habit_obj = self.habits[name]
        if not habit_obj.is_checked_off():
            return False
        habit_obj.uncheck_habit()
        update_habit_history(self.db_name, habit_obj)
        return True

    def data_as_dict(self):
        """ Returns the habit data as a dictionary of habit objects.
        For usage in Analytics module.

        :return: dictionary of habit objects
        :rtype: dict
        """
        return self.habits.copy()
