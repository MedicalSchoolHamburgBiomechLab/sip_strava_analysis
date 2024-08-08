from db import init_db, Session
from models import *


def get_athletes() -> list[dict]:
    session = Session()
    athletes = session.query(AthleteModel).all()
    athletes_dict = [athlete.to_dict() for athlete in athletes]
    session.close()
    return athletes_dict


def get_streams_by_type(stream_type: str) -> list[dict]:
    session = Session()
    streams = session.query(StreamModel).filter_by(stream_type=stream_type).all()
    streams_dict = [stream.to_dict() for stream in streams]
    session.close()
    return streams_dict


if __name__ == '__main__':
    init_db()
    athletes = get_athletes()
    heartrate_streams = get_streams_by_type('heartrate')
    # ... and so on
