import questionary as qt

class HabitTrackerCLI:

  def __init__(self):

    self.loop = True
    pass

  # Support methods

  def get_habit_details(self):
    pass

  # Main methods

  def cli_add_habit(self):
    pass

  def cli_edit_habit(self):
    pass

  def cli_checkoff_today_habits(self):
    pass
  
  def remove_habits(self):

    #a = #get list of all habbits
    #ask question about
    #HabbitTracker()
    #delete the selected habbits
    pass
  
  def view_habits(self):

    #Analytis.view all habits tabulate
    pass

  def view_analytics(self):

    #A folder for analytics module
    pass

  def exit(self):
    self.loop = False
    pass


  def main_loop(self):

    while self.loop:

      print('Main Menu:')

      menu = {
        'Check off Habits!' : self.cli_checkoff_habits,
        'Add a new Habit' : self.cli_add_habit,
        'Edit Habits' : self.cli_edit_hait,
        'View all habits' : self.cli_view_habits,
        'Analytics!' : self.cli_view_analytics,
        'Exit' : self.cli_exit
        }
      
      option = qt.select("What do you like to do?", choices = menu.index).ask()
        
      func = menu[option]
      func()
