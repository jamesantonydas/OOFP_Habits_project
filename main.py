from src.HabitTrackerCLI import *
from src.HabitManager import *
import logging


def main() -> None:
    """ Main entry point of the application"""

    logging.basicConfig(filemode = "habit_log.log", level=logging.ERROR)

    habit_manager = HabitManager("Habit_data.db")
    habit_manager.load_habits_from_db()
    habit_cli = HabitTrackerCLI(habit_manager)
    habit_cli.main_loop()


if __name__ == "__main__":
    main()
