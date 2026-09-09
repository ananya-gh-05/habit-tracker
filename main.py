import sys
from PySide6.QtWidgets import QApplication,QWidget,QCheckBox,QVBoxLayout,QLabel,QPushButton,QInputDialog,QHBoxLayout
from database import create_tables,local_session
from models import Habit,HabitCompletion
from datetime import datetime,date,timedelta


#adding a new habit
def add_habit():
    name,ok=QInputDialog.getText(window,"Add Habit","Enter the habit name:")
    if ok and name:
        session=local_session()

        habit=Habit(name=name)
        session.add(habit)
        session.commit()

        habit_id=habit.id
        session.close()
        row=QHBoxLayout()

        checkbox=QCheckBox(str(habit.name))
        delete_button=QPushButton("Delete")
        checkbox.stateChanged.connect(
            lambda state,habit_id=habit_id:
                habit_checked(state,habit_id)
            )

        delete_button.clicked.connect(
            lambda checked=False,
            habit_id=habit_id,
            checkbox=checkbox,
            delete_button=delete_button:
                delete_habit(habit_id,checkbox,delete_button)
        )

        row.addWidget(checkbox)
        row.addWidget(delete_button)
        layout.insertLayout(layout.indexOf(add_button),row)


create_tables()

app=QApplication(sys.argv)

window=QWidget()
window.setWindowTitle("Habit Tracker")
window.resize(300,200)

layout=QVBoxLayout()

title=QLabel("Habit Tracker")
layout.addWidget(title)


#loading the tasks
def load_habits():
    session=local_session()
    habits=session.query(Habit).all()
    for habit in habits:
        row=QHBoxLayout()

        checkbox=QCheckBox(str(habit.name))

        delete_button=QPushButton("Delete")

        completion=session.query(HabitCompletion).filter(HabitCompletion.habit_id==habit.id, HabitCompletion.completed_at>=date.today()).first()
        if completion:
            checkbox.setChecked(True)

        checkbox.stateChanged.connect(
            lambda state,habit_id=habit.id: habit_checked(state,habit_id)
        )

        delete_button.clicked.connect(
            lambda checked=False, habit_id=habit.id,checkbox=checkbox,delete_button=delete_button:
                delete_habit(habit_id,checkbox,delete_button)
        )
        row.addWidget(checkbox)
        row.addWidget(delete_button)

        layout.addLayout(row)
    session.close()


#logging completion of a habit
def habit_checked(checked,habit_id):
    session=local_session()
    today_start=datetime.combine(date.today(),datetime.min.time())
    tomorrow_start=today_start+timedelta(days=1)

    completion=session.query(HabitCompletion).filter(
            HabitCompletion.habit_id==habit_id,
            HabitCompletion.completed_at>=today_start,
            HabitCompletion.completed_at<tomorrow_start
        ).first()

    if checked:
        if not completion:
            completion=HabitCompletion(habit_id=habit_id,completed_at=datetime.now())
            session.add(completion)
            session.commit()

    else:
        if completion:
            session.delete(completion)
            session.commit()

    session.close()



study=QCheckBox("Study")
dsa=QCheckBox("DSA")
exercise=QCheckBox("Exercise")
walk=QCheckBox("Walk")
water=QCheckBox("Water")
project=QCheckBox("project")

layout.addWidget(study)
layout.addWidget(dsa)
layout.addWidget(exercise)
layout.addWidget(walk)
layout.addWidget(water)
layout.addWidget(project)

load_habits()


#deleting a habit
def delete_habit(habit_id,checkbox,delete_button):
    session=local_session()

    completions=session.query(HabitCompletion).filter_by(habit_id=habit_id).all()

    for completion in completions:
        session.delete(completion)

    habit=session.query(Habit).filter_by(id=habit_id).first()
    if habit:
        session.delete(habit)

    session.commit()
    session.close()
    checkbox.deleteLater()
    delete_button.deleteLater()


#add button
add_button=QPushButton("Add Habit")
add_button.clicked.connect(add_habit)
layout.addWidget(add_button)

window.setLayout(layout)
window.show()
sys.exit(app.exec())
