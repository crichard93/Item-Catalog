from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Brand, Model, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///cars.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Display All Brands
@app.route('/')
@app.route('/brands/')
def showBrands():
    brands = session.query(Brand).order_by(asc(Brand.name))
    return render_template('showBrands.html', brands = brands)


#Display all Models in brand with options to delete, or add Models
@app.route('/brands/<int:brand_id>')
def showModels(brand_id):
	brand = session.query(Brand).filter_by(id = brand_id)
	models = session.query(Model).filter_by(brand_id = brand_id)
	return render_template('showModels.html', brand = brand, models = models)

#Display description + image of Model in a Brand with option to Edit or delete

#Edit Model in Brand

#

#Delete Model from Brand

#Display Model Description + Image with Options to delete or edit




#Login

#Disconnect

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)