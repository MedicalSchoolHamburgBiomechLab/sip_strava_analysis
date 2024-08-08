import pickle

from sqlalchemy import Column, Integer, ForeignKey, String, BLOB

from db import Base, Session


class StreamModel(Base):
    __tablename__ = 'streams'

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey('activities.id'))
    stream_type = Column(String)
    stream_data = Column(BLOB)

    def __init__(self, activity_id, stream_type, stream_data):
        self.activity_id = activity_id
        self.stream_type = stream_type
        self.stream_data = pickle.dumps(stream_data)

    def __repr__(self):
        return f'<StreamModel {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'activity_id': self.activity_id,
            'stream_type': self.stream_type,
            'stream_data': pickle.loads(self.stream_data)
        }

    def save(self):
        session = Session()
        session.add(self)
        session.commit()

    @classmethod
    def find_by_stream_type(cls, stream_type: str):
        session = Session()
        result = session.query(cls).filter_by(stream_type=stream_type).first()
        session.close()
        return result
