from sqlalchemy import Column, Integer, String
from database import Base


class Resource(Base):
    __tablename__ = 'resource'

    unique_id = Column(String(50), primary_key=True)
    name = Column(String(50))
    hours = Column(Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, unique_id=None, name=None, hours=None):
        self.unique_id = unique_id
        self.name = name
        self.hours = hours

    def __repr__(self):
        return f'<Resource {self.name!r}>'
