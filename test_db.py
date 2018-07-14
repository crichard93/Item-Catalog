"""Test data to ensure it was added successfully. """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Model, User, Brand, Base

#Open a DB session named session
engine = create_engine('sqlite:///cars.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Test DB for successful additions
models = session.query(Model).all()
brands = session.query(Brand).all()
users = session.query(User).all()
for model in models:
    print model.name
    print model.description
    print model.user_id
    print model.image

for brand in brands:
    print brand.name
    print brand.user_id

for user in users:
    print user.name
    print user.email