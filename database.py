from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

DATABASE_URL="sqlite:///habits.db"
engine=create_engine(DATABASE_URL)
local_session=sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)


if __name__=="__main__":
    create_tables()
    print("Database and tables are created!")
