import sys
from PySide6.QtWidgets import QApplication,QWidget,QCheckBox,QVBoxLayout,QLabel,QPushButton,QInputDialog,QHBoxLayout,QMessageBox,QDialog,QListWidget
from PySide6.QtCore import Qt
from database import create_tables,local_session
from models import Habit,HabitCompletion
from datetime import datetime,date,timedelta


#adding a new habit
def add_habit():
    name,ok=QInputDialog.getText(window,"Add Habit","Enter the habit name:")
    if ok and name.strip():
        session=local_session()

        #check if any same existing habits
        existing_habit=session.query(Habit).filter(
            Habit.name.ilike(name.strip())
        ).first()
        if existing_habit:
            QMessageBox.warning(window,"Duplicate detected","This habit already exists!")
            session.close()
            return


        habit=Habit(name=name.strip())
        session.add(habit)
        session.commit()

        session.close()
        load_habits()


create_tables()

app=QApplication(sys.argv)

window=QWidget()
window.setWindowTitle("Habit Tracker")

#themes and stuff
window.setStyleSheet("""
    QWidget{
        background-color:#DCEEFF;
    }
    QLabel {
        color:#123B66;
    }
    QLabel#title {
        font-size: 20px;
        font-weight: bold;
        color: #344E41;
        margin-top: 15px;
        margin-bottom: 15px;
        padding: 0px;
        margin: 0px;
    }
    QCheckBox {
        color: #000000;
        spacing: 8px;
    }
    QPushButton {
        background-color: #245A91;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 6px 12px;
    }
    QPushButton:hover {
        background-color: #174573;
    }
    QPushButton:pressed {
        background-color: #103557;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #52796F;
        border-radius: 4px;
        background-color: white;
    }
    QCheckBox::indicator:checked {
        background-color: #52796F;
        border: 2px solid #52796F;
        image:url(dark_tick.svg);
    }
    QInputDialog {
        color: #000000;
    }
    QInputDialog QLabel {
        color: #000000;
    }
    QInputDialog QLineEdit {
        color: #000000;
        background-color: white;
    }
    """)
window.resize(400,200)

layout=QVBoxLayout()
habit_layout=QVBoxLayout()

#handle the spacing
layout.setSpacing(6)
layout.setContentsMargins(20,10,20,10)

#title
title=QLabel("Habit Tracker")
title.setObjectName("title")
title.setAlignment(Qt.AlignCenter)
title.setFixedHeight(35) #to not allocate more than needed height
layout.addWidget(title)
layout.addLayout(habit_layout)


#helper func to load_habits()
def clear_habit_layout():
    while habit_layout.count():
        item=habit_layout.takeAt(0)

        if item.layout():
            row=item.layout()
            while row.count():
                child=row.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        elif item.widget():
            item.widget().deleteLater()


#loading the tasks
def load_habits():
    clear_habit_layout()
    session=local_session()
    habits=session.query(Habit).all()
    if(habits):
        for habit in habits:
            row=QHBoxLayout()

            checkbox=QCheckBox(str(habit.name))

            delete_button=QPushButton("Delete")

            completion=session.query(HabitCompletion).filter(HabitCompletion.habit_id==habit.id,HabitCompletion.completed_at==date.today()).first()

            if completion:
                checkbox.setChecked(True)

            checkbox.toggled.connect(
                lambda checked,habit_id=habit.id:
                    habit_checked(checked,habit_id)
            )

            delete_button.clicked.connect(
                lambda checked=False, habit_id=habit.id:
                    delete_habit(habit_id)
            )
            row.addWidget(checkbox)
            row.addWidget(delete_button)

            habit_layout.addLayout(row)

    else:
        # display No habits available
        no_habits=QLabel("No habits available!")
        no_habits.setAlignment(Qt.AlignCenter)
        habit_layout.addWidget(no_habits)

    session.close()


#logging completion of a habit
def habit_checked(checked,habit_id):
    print("Habit ID:",habit_id)
    print("Checked:",checked)

    session=local_session()

    completion=session.query(HabitCompletion).filter(
        HabitCompletion.habit_id==habit_id,
        HabitCompletion.completed_at==date.today()
    ).first()

    if checked:
        if not completion:
            completion=HabitCompletion(
                habit_id=habit_id,
                completed_at=date.today()
            )
            session.add(completion)
            print("Completion added")
        else:
            print("Completion already exists")
    else:
        if completion:
            session.delete(completion)
            print("Completion deleted")
        else:
            print("No completion found to delete")

    session.commit()

    remaining=session.query(HabitCompletion).filter(
        HabitCompletion.habit_id==habit_id,
        HabitCompletion.completed_at==date.today()
    ).count()

    print("Today's completion records remaining:",remaining)

    session.close()


#deleting a habit
def delete_habit(habit_id):
    session=local_session()

    completions=session.query(HabitCompletion).filter_by(habit_id=habit_id).all()

    for completion in completions:
        session.delete(completion)

    habit=session.query(Habit).filter_by(id=habit_id).first()
    if habit:
        session.delete(habit)

    session.commit()
    session.close()
    load_habits()


#view history
def view_history():
    history_window=QDialog(window)
    history_window.setWindowTitle("Habit History")
    history_window.resize(350,400)
    history_window.setStyleSheet("""
        QDialog {
            background-color: #DCEEFF;
        }
        QListWidget {
            background-color: #DCEEFF;
            color: #123B66;
            border: 3px solid #52796F;
            border-radius: 8px;
            padding: 8px;
        }
    """)
    history_layout=QVBoxLayout()
    history_list=QListWidget()
    history_list.setStyleSheet("""
        QListWidget {
            background-color: #DCEEFF;
            color: #123B66;
            border: 3px solid #52796F;
        }
    """)

    session=local_session()
    habits=session.query(Habit).all()

    if not habits:
        history_list.addItem("No Habits available!")
    else:
        for habit in habits:
            history_list.addItem(habit.name)

            completions=session.query(HabitCompletion).filter(
                HabitCompletion.habit_id==habit.id
            ).order_by(HabitCompletion.completed_at.desc()).all()
            if completions:
                for completion in completions:
                    history_list.addItem(f"  Completed: {completion.completed_at}")
            else:
                history_list.addItem("No completions yet!")

            history_list.addItem("")

    session.close()
    history_layout.addWidget(history_list)
    history_window.setLayout(history_layout)
    history_window.exec()

#buttons section
button_layout=QHBoxLayout()

#add button
add_button=QPushButton("Add Habit")
add_button.clicked.connect(add_habit)
button_layout.addWidget(add_button)

#history button
history_button=QPushButton("View History")
history_button.clicked.connect(view_history)
button_layout.addWidget(history_button)

layout.addLayout(button_layout)


load_habits()

window.setLayout(layout)
window.show()
sys.exit(app.exec())
