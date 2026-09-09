from sqlalchemy import Column,Integer,String,DateTime,Date
from datetime import datetime,date
from sqlalchemy.orm import declarative_base

Base=declarative_base()

class Habit(Base):
    __tablename__="habits"

    id=Column(Integer,primary_key=True)
    name=Column(String(100),nullable=False)
    created_at=Column(DateTime,default=datetime.now)

class HabitCompletion(Base):
    __tablename__="habit_completions"

    id=Column(Integer,primary_key=True)
    habit_id=Column(Integer,nullable=False)
    completed_at=Column(Date,default=date.today)
