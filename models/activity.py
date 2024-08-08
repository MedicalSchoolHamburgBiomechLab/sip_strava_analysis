from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from db import Base, Session


class ActivityModel(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    strava_activity_id = Column(Integer)
    athlete_id = Column(Integer, ForeignKey('athletes.id'))
    distance = Column(Float)
    moving_time = Column(Integer)
    total_elevation_gain = Column(Float)
    activity_type = Column(String)
    start_date = Column(DateTime)
    start_date_local = Column(DateTime)
    streams = relationship('StreamModel', backref='activity', lazy=True)

    def __init__(self, athlete_id,
                 strava_activity_id,
                 distance,
                 moving_time,
                 total_elevation_gain,
                 activity_type,
                 start_date,
                 start_date_local):
        # Read the activity data
        self.strava_activity_id = strava_activity_id
        self.athlete_id = athlete_id
        self.distance = distance
        self.moving_time = moving_time
        self.total_elevation_gain = total_elevation_gain
        self.activity_type = activity_type
        self.start_date = start_date
        self.start_date_local = start_date_local

    def __repr__(self):
        return f'<ActivityModel {self.strava_activity_id}>'

    def to_dict(self):
        return {
            'strava_activity_id': self.strava_activity_id,
            'athlete_id': self.athlete_id,
            'distance': self.distance,
            'moving_time': self.moving_time,
            'total_elevation_gain': self.total_elevation_gain,
            'activity_type': self.activity_type,
            'start_date': self.start_date,
            'start_date_local': self.start_date_local,
            'streams': [stream.to_dict() for stream in self.streams] if self.streams else []
        }

    def save(self):
        session = Session()
        session.add(self)
        session.commit()

    @classmethod
    def find_by_strava_activity_id(cls, strava_activity_id: int):
        session = Session()
        result = session.query(cls).filter_by(strava_activity_id=strava_activity_id).first()
        return result
