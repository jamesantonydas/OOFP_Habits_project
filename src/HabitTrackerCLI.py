from src.Analytics import *
from src.Interface import *
import os
import logging


class HabitTrackerCLI:

    def __init__(self, habit_manager: HabitManager):

        self.loop = True
        self.habit_manager = habit_manager

    @staticmethod
    def clear_screen() -> None:
        """ Clears the screen of command line interface """
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except OSError:
            return

    def __cli_add_habit(self):
        """ Implements CLI interface for add habit functionality.

        :return: True if successfully added, False otherwise.
        """
        habit_name = ask_habit_name()
        if self.habit_manager.is_habit_exist(habit_name):
            print('The Habit already already exists! Please enter a new name..')
            return False
        habit_desc = ask_habit_desc()
        habit_periodicity = ask_habit_periodicity()
        self.habit_manager.add_habit(habit_name, habit_desc, HabitPeriods(habit_periodicity))
        return True

    def __cli_checkoff_today_habits(self):
        """ Implements CLI interface for checking off functionality

        :returns: None
        """
        menu_list = list_currently_unchecked_habits(list(self.habit_manager.habits.values()))
        habits_to_checkoff = qt.checkbox('Please select the Habits you wish to check off! ',
                                         choices = menu_list).ask()
        self.habit_manager.check_off_habits(habits_to_checkoff)
        return None

    def __cli_view_analytics(self):
        """ Implements CLI interface for habit analytics

        :returns: None
        """
        habit_list: list = list(self.habit_manager.habits.values())
        habit_sorted = sorted(habit_list, key = lambda x: x.habit_streak()[0], reverse = True)

        habit_daily = list_habit_with_periodicity(habit_sorted, HabitPeriods.DAILY)
        habit_weekly = list_habit_with_periodicity(habit_sorted, HabitPeriods.WEEKLY)
        habit_monthly = list_habit_with_periodicity(habit_sorted, HabitPeriods.MONTHLY)
        habit_yearly = list_habit_with_periodicity(habit_sorted, HabitPeriods.YEARLY)

        table_style = "mixed_grid"
        headers = ['Name', '\N{Fire}', '\N{sunflower}',
                   '\N{snowflake}', '\N{snowflake}\N{snowflake}', '\N{sparkles}',
                   '\N{alarm clock}']

        if len(habit_daily) > 1:
            print("\n Habits with Daily Periodicity: " + str(len(habit_daily)) + "\n")
            table_data = list_habit_analytics_table(self.habit_manager.data_as_dict(), habit_daily)
            print(tabulate(table_data, headers, tablefmt = table_style))

        if len(habit_weekly) > 1:
            print("\n Habits with Weekly Periodicity: " + str(len(habit_weekly)) + "\n")
            table_data = list_habit_analytics_table(self.habit_manager.data_as_dict(), habit_weekly)
            print(tabulate(table_data, headers, tablefmt = table_style))

        if len(habit_monthly) > 1:
            print("\n Habits with Monthly Periodicity: " + str(len(habit_monthly)) + "\n")
            table_data = list_habit_analytics_table(self.habit_manager.data_as_dict(), habit_monthly)
            print(tabulate(table_data, headers, tablefmt = table_style))

        if len(habit_yearly) > 1:
            print("\n Habits with Yearly Periodicity: " + str(len(habit_yearly)) + "\n")
            table_data = list_habit_analytics_table(self.habit_manager.data_as_dict(), habit_yearly)
            print(tabulate(table_data, headers, tablefmt = table_style))

        print("\nLegend")
        print("\N{Fire} :", "Current Streak")
        print("\N{sunflower} :", "Longest Streak")
        print("\N{snowflake}  :", "Longest Break")
        print("\N{snowflake}\N{snowflake} :", "Total Breaks")
        print("\N{sparkles} :", "Total check-offs")
        print("\N{alarm clock} :", "Total Duration")

        return

    def __cli_exit(self):
        """ Exit the application"""
        self.loop = False
        return None

    def __cli_view_edit_habit(self):
        """ Implements Edit menu for CLI interface"""

        def __just_return(name: str, temp: HabitManager):
            """ Function for simply return to the main menu"""
            return None

        menu = {
            'View Habit Analytics': habit_report_one,
            'Check / Uncheck the Habit for today?!': check_or_uncheck_habit,
            'Rename the Habit': rename_habit,
            'Edit Description': edit_habit_desc,
            'Change periodicity': edit_habit_periodicity,
            'Reset the Habit': reset_habit,
            'Delete the Habit': delete_habit,
            'Return to the main menu': __just_return
        }

        self.clear_screen()
        habit_names = list_currently_tracked_habits(list(self.habit_manager.habits.values()))
        habit_info_list = list_habit_info(self.habit_manager.data_as_dict(), habit_names)
        habit_to_edit = qt.select("Please select the Habit to View / Edit:", choices = habit_info_list).ask()
        selected_habit = habit_names[habit_info_list.index(habit_to_edit)]
        print("\n Selected habit: ", selected_habit)
        task_edit = qt.select("What do you like to do? ", choices = list(menu.keys())).ask()
        func = menu[task_edit]
        func(selected_habit, self.habit_manager)

    def main_loop(self):
        """ Main menu of the application

        :returns: None
        """

        while self.loop:

            self.clear_screen()
            n_tasks: int = len(self.habit_manager.habits)
            print("Habit Tracker")
            print(f"\n You are tracking {n_tasks} Habits! Let's do more!")
            print("\N{Fire} :", "Current Streak", "\N{sunflower} :", "Longest Streak")
            habit_names = list_currently_tracked_habits(list(self.habit_manager.habits.values()))
            habit_info_list = list_habit_info(self.habit_manager.data_as_dict(), habit_names)
            habit_info_table = [[x] for x in habit_info_list]
            print(tabulate(habit_info_table, headers = ['currently tracked Habits'], tablefmt = 'mixed_grid'))

            menu = {
                'Add a new Habit': self.__cli_add_habit,
                'View/Edit Habits': self.__cli_view_edit_habit,
                'Check off habits!': self.__cli_checkoff_today_habits,
                'View Analytics!': self.__cli_view_analytics,
                'Exit': self.__cli_exit
            }

            option = qt.select("What do you like to do?", choices = list(menu.keys())).ask()

            try:
                func = menu[option]
                func()
                input('Press any key to continue...')
            except Exception as e:
                print("\nERROR: Something went wrong!\n", str(e))
                logging.error("Exception:" + str(e))

        return None
