# Habit Tracker

A simple desktop habit tracker built with Python, PySide6, SQLAlchemy, and SQLite.

The application allows users to create and manage habits and track their daily completion through a simple desktop interface.

## Current Features

* Add new habits
* Display saved habits from the database
* Mark habits as completed
* Unmark completed habits
* Delete habits
* Persist habit data using SQLite
* Simple desktop GUI using PySide6

## Tech Stack

* **Python**
* **PySide6** — Desktop GUI
* **SQLAlchemy** — Database ORM
* **SQLite** — Local database
* **Git & GitHub** — Version control


## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/ananya-gh-05/habit-tracker.git
cd habit-tracker
```

### 2. Install dependencies

```bash
pip install PySide6 SQLAlchemy
```

### 3. Run the application

```bash
python main.py
```

The SQLite database will be created locally when the application is initialized.

## Database

The application uses SQLite for local data storage and SQLAlchemy for database interaction.

The main database entities are:

* `Habit` — Stores habit information
* `HabitCompletion` — Stores habit completion information

The database file is excluded from Git using `.gitignore`.

## Future Improvements

* Date-specific habit completion tracking
* Habit streak tracking
* Daily/weekly progress statistics
* Progress dashboard
* Habit editing
* Better UI styling
* Notifications and reminders
* Habit completion history
* Data visualization
* Packaging the application as a Windows executable

## Status

🚧 **In Development**

This project is being developed incrementally as a personal desktop habit-tracking application.
