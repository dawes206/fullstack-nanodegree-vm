import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key=True)

    # @property
    # def serialize(self):
    #     #returns object data in easily seializable format
    #     return {
    #             'name': self.name,
    #             'description': self.description,
    #             'id': self.id
    #         }

class Items(Base, ):
    __tablename__ = 'bushcrafting_items'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    category = Column(String(250))
    weight = Column(Float)
    volume = Column(Float)
    amount = Column(Integer)
    packed = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship(User)

    # @property
    # def serialize(self):
    #     #returns object data in easily seializable format
    #     return {
    #             'name': self.name,
    #             'description': self.description,
    #             'id': self.id,
    #             'price': self.price,
    #             'course': self.course,
    #         }


engine = create_engine('sqlite:///bushcrafting.db')

Base.metadata.create_all(engine)
