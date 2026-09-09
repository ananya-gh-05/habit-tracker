from database import local_session
from models import Habit,HabitCompletion


session = local_session()

habits = session.query(Habit).all()
habitcompleted=session.query(HabitCompletion).all()

print("ALL HABITS:")
for habit in habits:
    print(habit.id,habit.name,habit.created_at)

print("COMPLETIONS:")
for habit in habitcompleted:
    print(habit.id,habit.habit_id,habit.completed_at)

session.close()
