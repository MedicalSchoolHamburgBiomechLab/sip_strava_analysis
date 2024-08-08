from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

DATABASE_URL = 'sqlite:///sip_strava.db'


engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
metadata = MetaData()


def init_db():
    Base.metadata.create_all(engine)
