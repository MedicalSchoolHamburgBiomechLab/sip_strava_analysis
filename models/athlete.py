from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, joinedload

from db import Base, Session


class AthleteModel(Base):
    __tablename__ = 'athletes'

    id = Column(Integer, primary_key=True)
    subject_id = Column(String(4), unique=True, nullable=False)
    strava_id = Column(Integer)
    activities = relationship('ActivityModel', backref='athlete', lazy=True)

    def __init__(self, strava_id: int, subject_id: str):
        self.strava_id = strava_id
        self.subject_id = subject_id

    def __repr__(self):
        return f'<AthleteModel {self.subject_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'subject_id': self.subject_id,
            'strava_id': self.strava_id,
            'activity_count': len(self.activities)
        }

    @classmethod
    def find_by_subject_id(cls, subject_id: str):
        session = Session()
        result = session.query(cls).filter_by(subject_id=subject_id).first()
        session.close()
        return result

    @classmethod
    def find_all(cls):
        session = Session()
        result = session.query(cls).options(joinedload(cls.activities)).all()
        session.close()
        return result

    def save(self):
        session = Session()
        session.add(self)
        session.commit()
