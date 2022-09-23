from .models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///database/db.sqlite3")

SessionMaker = sessionmaker(bind=engine)


def create_database_metadata():
    DeclarativeBase.metadata.create_all(bind=engine)
