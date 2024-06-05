from src.Habit import *


def sample_habits() -> list:
    """ Builds sample data for the tracker application

    :return: list of habit objects
    :rtype: list[Habit]
    """
    h1 = Habit("Drink 8 glasses of water",
               description = "Stay hydrated, and be more healthy",
               periodicity = HabitPeriods.DAILY, creation_date = '2024-06-01',
               history = "2024-06-01,2024-06-02,2024-06-03,2024-06-05,2024-06-06")
    h2 = Habit("Meditate for 5 minutes",
               description = "Let's keep our mind free and focused",
               periodicity = HabitPeriods.DAILY, creation_date = '2024-06-01',
               history = "2024-06-01,2024-06-03,2024-06-04")
    h3 = Habit("Take a short walk",
               description = "This might help use improve our mood",
               periodicity = HabitPeriods.DAILY, creation_date = '2024-05-29',
               history = "2024-05-29,2024-05-30,2024-06-01,2024-06-02,2024-06-03")
    h4 = Habit("Plan my weekly goals",
               description = "Time to focus on the work more!",
               periodicity = HabitPeriods.WEEKLY, creation_date = '2024-04-01',
               history = "2024-04-03,2024-04-10,2024-04-17,2024-04-24")
    h5 = Habit("Try a new recipie",
               description = "try to cook it too.. :)",
               periodicity = HabitPeriods.WEEKLY, creation_date = '2024-01-01',
               history = "2024-01-01,2024-02-02,2024-05-30,2024-06-06")
    h6 = Habit("Read a full book",
               description = "Well, it's time to work on that reading goal",
               periodicity = HabitPeriods.MONTHLY, creation_date = '2024-01-01',
               history = "2024-01-01,2024-02-02,2024-03-25,2024-04-14")
    h7 = Habit("Review monthly bills",
               description = "Improving our budgeting skills helps.",
               periodicity = HabitPeriods.MONTHLY, creation_date = '2024-01-01',
               history = "2024-01-01,2024-02-05,2024-04-16,2024-05-15,2024-06-02")
    h8 = Habit("Plan and take a vacation",
               description = "relax and take a vacation, we can get back to work with more energy!",
               periodicity = HabitPeriods.YEARLY, creation_date = '2022-01-01',
               history = "2023-01-01,2024-02-02")

    return [h1, h2, h3, h4, h5, h6, h7, h8]
