"""This file creates the database for the Item Catalog Project"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()


#Format for User table
class User(Base):
    __tablename__ ='user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


#Format for CarType Table
class CarType(Base):
    __tablename__ = 'car_type'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    #Return data in serializable format for JSON endpoint
    @property
    def serialize(self):
       return {
           'name'         : self.name,
           'id'           : self.id,
       }


#Format for Car Table 
class Car(Base):
    __tablename__ = 'car'


    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    image = Column(String(250))
    car_type_id = Column(Integer,ForeignKey('car_type.id'))
    car_type = relationship(CarType)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    #Return data in serializable format for JSON endpoint
    @property
    def serialize(self):
       return {
           'name'         : self.name,
           'description'  : self.description,
           'id'           : self.id,
           'image'        : self.image
       }



engine = create_engine('sqlite:///cars.db')
 

Base.metadata.create_all(engine)
