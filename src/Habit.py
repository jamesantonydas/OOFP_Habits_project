from enum import Enum
from datetime import datetime
import logging


class HabitPeriods(Enum):
    # Enum for representing habit periodicity

    DAILY: str = 'daily'
    WEEKLY: str = 'weekly'
    MONTHLY: str = 'monthly'
    YEARLY: str = 'yearly'


class HabitError(Exception):
    # Custom Habit Exception

    def __init__(self, message):
        """Handles custom Exception for Habit Class

        :param str message: Message from the exception.
        :return: The function returns nothing
        """
        super().__init__(message)


class Habit:

    def __init__(self, name: str, description: str = "", periodicity: HabitPeriods = HabitPeriods.DAILY,
                 creation_date: str = "", history: str = ""):
        """ Initializes the Habit Object

        :param str name: Name of the Habit Object
        :param str description: Additional Description of the Habit Object
        :param HabitPeriods periodicity: Accepts HabitPeriods as periodicity (Default is daily)
        :param str creation_date: The date of creation in "%Y-%m-%d" format (Default is current date)
        :param str history: A string of dates in "%Y-%m-%d,%Y-%m-%d" format
        :returns: The function returns nothing
        """

        self.name: str = name
        self.description: str = description
        self.periodicity: HabitPeriods = periodicity
        self.creation_date: datetime = datetime.now()
        self.habit_history: list = []

        # loading the history data
        if history != "":
            history = history.split(',')
            for dates in history:
                self.habit_history.append(datetime.strptime(dates, '%Y-%m-%d'))

        # loading the creation date
        if creation_date != "":
            self.creation_date = datetime.strptime(creation_date, '%Y-%m-%d')

    def __calculate_duration(self, recent_date: datetime, older_date: datetime) -> int:
        """ Calculates the number of days between two given dates.

        :param datetime recent_date: The recent date to be subtracted from.
        :param datetime older_date: The older date to be subtracted by.
        :return: The number of days between two dates
        :rtype: int
        """

        time_diff = 0
        if self.periodicity == HabitPeriods.DAILY:
            time_diff = (recent_date - older_date).days
        elif self.periodicity == HabitPeriods.WEEKLY:
            time_diff = (recent_date - older_date).days / 7
        elif self.periodicity == HabitPeriods.MONTHLY:
            time_diff = (recent_date.year - older_date.year) * 12 + recent_date.month - older_date.month
        elif self.periodicity == HabitPeriods.YEARLY:
            time_diff = recent_date.year - older_date.year
        return time_diff

    def habit_streak(self):
        """ Calculates the habit Streak of the Habit Object

        :param: the function accepts no arguments.
        :return: The current habit streak and longest habit streak.
        :rtype: float, float
        :raises HabitError: Raises exceptions when there is an irregularity in history
        """
        current_streak = 1
        longest_streak = 1
        h_dates = self.habit_history

        if not h_dates:
            return 0, 0

        for i in range(1, len(h_dates)):

            time_diff = self.__calculate_duration(h_dates[i], h_dates[i-1])
            if time_diff == 1:
                current_streak += 1
                longest_streak = max(current_streak, longest_streak)
            elif time_diff < 0:
                logging.error("Irregular dates")
                raise HabitError("Error: Irregular dates in " + self.name + "\n Try resetting the history.")
            else:
                current_streak = 1

        # difference between today and the last entry
        diff = self.__calculate_duration(datetime.now(), h_dates[-1])
        if diff > 1:
            current_streak = 0
        elif diff < 0:
            logging.error("Irregular dates")
            raise HabitError("Error: Irregular dates in " + self.name + "\n Try resetting the history.")

        return current_streak, longest_streak

    def habit_breaks(self):
        """ Calculates Longest habit breaks and the total number of habit breaks in the given Habit object.

        :param: the function accepts no arguments.
        :return: the longest habit break, and total number of habit breaks.
        :rtype: float, float
        :raises HabitError: Raises exception when irregularity is detected.
        """

        total_breaks = 0
        longest_break = 1
        h_dates = self.habit_history

        if not h_dates:
            return 0, 0

        for i in range(1, len(h_dates)):

            time_diff = self.__calculate_duration(h_dates[i], h_dates[i-1])
            if time_diff > 1:
                total_breaks += 1
                current_break = time_diff - 1
                longest_break = max(current_break, longest_break)
            elif time_diff < 0:
                logging.error("Irregular dates")
                raise HabitError("Error: Irregular dates in " + self.name + "\n Try resetting the history.")

        # difference between today and the last entry
        diff = self.__calculate_duration(datetime.now(), h_dates[-1])
        if diff > 1:
            total_breaks += 1
            current_break = diff - 1
            longest_break = max(current_break, longest_break)
        elif diff < 0:
            logging.error("Irregular dates")
            raise HabitError("Error: Irregular dates in " + self.name + "\n Try resetting the history.")

        return longest_break, total_breaks

    def habit_stats(self):
        """ Calculates the total number of check off entries, and total duration

        :return: total number of check offs, total duration of the habit till today.
        :rtype: float, float
        :raises HabitError: when irregularities found in the Habit history.
        """

        if not self.habit_history:
            return 0, 0
    
        total_checkoffs = len(self.habit_history)
    
        first_entry = self.creation_date
        last_entry = datetime.now()
        total_duration: int = self.__calculate_duration(last_entry, first_entry)
        
        if total_duration < 0:
            logging.error("Irregular dates")
            raise HabitError("Error: Irregular dates in " + self.name + "\n Try resetting the history.")
    
        return total_checkoffs, total_duration + 1

    def is_checked_off(self) -> bool:
        """ Checks to see if the given Habit is checked off for today.

        :return: True if the habit is checked off for today, False otherwise.
        :rtype: bool
        """

        if not self.habit_history:
            return False

        today = datetime.now()
        last_entry = self.habit_history[-1]

        total_duration = self.__calculate_duration(today, last_entry)

        if total_duration == 0:
            return True
        else:
            return False

    def check_off(self) -> bool:
        """ Checks off the given Habit Object for today

        :return: True if habit is successfully checked off, False otherwise.
        :rtype: bool
        """

        if not self.is_checked_off():
            self.habit_history.append(datetime.now())
            return True
        else:
            return False

    def uncheck_habit(self) -> bool:
        """ Uncheck off the given Habit object for today

        :return: True if habit is successfully unchecked off, False otherwise.
        :rtype: bool
        """
        if not self.is_checked_off():
            return False
        self.habit_history.pop()
        return True

    def get_history(self) -> str:
        """ Exports history data of the object as a string

        :return: Returns Habit history data as a string in "%Y-%m-%d,%Y-%m-%d" format
        :rtype: str
        """

        history = []
        if not self.habit_history:
            return ""
        for date in self.habit_history:
            history.append(datetime.strftime(date, '%Y-%m-%d'))
        return ','.join(history)

    def set_history(self, history: str):
        """ Imports history data from a string

        :param str history: History data as a string in "%Y-%m-%d,%Y-%m-%d" format
        :return: returns True if string is successfully imported, False otherwise.
        :rtype: bool
        """

        if history == "":
            return False
        history = history.split(',')
        dates = []
        for date in history:
            dates.append(datetime.strptime(date, '%Y-%m-%d'))
        self.habit_history = dates
        return True

    def get_creation_date(self) -> str:
        """ Exports creation date as a string

        :return: Creation date as string in "%Y-%m-%d" format
        :rtype: str
        """
        return datetime.strftime(self.creation_date, '%Y-%m-%d')
