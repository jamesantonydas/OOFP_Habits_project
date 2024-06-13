# Habit Tracker Application
 (Under Development Phase)
This page will be updated along with proper documentation.

The Habit Tracker Application helps users build and track their habits. With habit tracker app, users can add habit (for example, take a walk everyday) and define their habit periodicities (daily, weekly, monthly and yearly). Users can check-off, or mark them completed every day or week, depending on the periodicity. Habit tracker gives them further analytics and insights into their habits.

<p align="center" width="40">
  <img src="https://github.com/jamesantonydas/OOFP_Habits_project/blob/main/docs/img/banner.png"/>
</p>

The Habit Tracker offers a simple and easy to use interface for habit building. 

## Getting Started

This project needs the python runtime installed in your system. 
You can install the latest version of python from python's official website.

### Downloading the application

You can download the application files from repository, or create a new folder and simply run the command,

```
git clone https://github.com/jamesantonydas/OOFP_Habits_project
```

### Installing the dependencies

After downloading the application, simply run the following command to install all the dependencies.

```
pip install -r requirements.txt
```

The application requires following dependencies,

1. Questionary - For commandline interface
2. Tabulate - For tabulating the data
3. Sqlite3 - For storing the database
4. Pytest - For unit testing the program
5. Freezegun - For freezing the time during unit-tests
### Running the program

To run the program, simply run,
```commandline
python main.py
```

### Running the tests

For running the unit-tests, simply run

```commandline
python -m pytest .
```

## UML Class diagram

<p align="center" width="10%">
  <img src="https://github.com/jamesantonydas/OOFP_Habits_project/blob/main/docs/img/OOFP%20class%20diagram.png" width="40%"/>
</p>



## Features

With HabitTracker The users can,
1. Add habits
2. Set the habit periodicity
3. Tracking the habits with analytics
4. View / Edit the tasks


