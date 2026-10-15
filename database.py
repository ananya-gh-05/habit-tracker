from sqlalchemy import create_engine,event
from sqlalchemy.orm import sessionmaker

from models import Base

engine=create_engine("sqlite:///habits.db")


@event.listens_for(engine,"connect")
def enable_foreign_keys(dbapi_connection,connection_record):
    cursor=dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

local_session=sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)


if __name__=="__main__":
    create_tables()
    print("Database and tables are created!")
