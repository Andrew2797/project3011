from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


engine = create_engine("postgresql+psycopg2://postgres:271197@localhost:5432/tours", echo=True)
#engine = create_engine("sqlite:///")
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def create_db():
    Base.metadata.create_all(bind=engine)
