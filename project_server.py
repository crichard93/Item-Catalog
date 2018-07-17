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
import os

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


#Display all Models in brand with options to add Models
@app.route('/brands/<int:brand_id>/')
def showModels(brand_id):
    brand = session.query(Brand).filter_by(id = brand_id).one()
    models = session.query(Model).filter_by(brand_id = brand_id)
    return render_template('showModels.html', brand = brand, models = models)

#Display description + image of Model in a Brand with option to Edit or delete
@app.route('/brands/<int:brand_id>/<int:model_id>/')
def showModel(brand_id, model_id):
    brand = session.query(Brand).filter_by(id = brand_id).one()
    model = session.query(Model).filter_by(id = model_id).one()
    return render_template('showModel.html', brand = brand, model = model)

#Edit Model in Brand, first show form, then edit and update database with form data
@app.route('/brands/<int:brand_id>/<int:model_id>/edit/',methods = ('GET', 'POST'))
@app.route('/brands/<int:brand_id>/<int:model_id>/edit/#',methods = ('GET', 'POST'))
def editModel(brand_id, model_id):
    brand = session.query(Brand).filter_by(id = brand_id).one()
    editModel = session.query(Model).filter_by(id = model_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editModel.name = request.form['name']
        if request.form['description']:
            editModel.description = request.form['description']
        session.add(editModel)
        session.commit
        return redirect(url_for('showModel', brand_id = brand_id, model_id = model_id))
    else:
        return render_template('editModel.html', brand = brand, editModel = editModel)

#Delete Model from Brand
@app.route('/brands/<int:brand_id>/<int:model_id>/delete/')
def deleteModel(brand_id, model_id):
    brand = session.query(Brand).filter_by(id = brand_id).one()
    model = session.query(Model).filter_by(id = model_id).one()
    return render_template('deleteModel.html', brand = brand, model = model)

#Add Model to Brand. First show the input form, then update database with form data from user
@app.route('/brands/<int:brand_id>/add/', methods = ('GET', 'POST'))
def addModel(brand_id):
    brand = session.query(Brand).filter_by(id = brand_id).one()
    if request.method == 'POST':
        newModel = Model(name = request.form['name'], description = request.form['description'], brand_id = brand_id, user_id = brand.user_id)
        session.add(newModel)
        session.commit()
        flash('New Model %s Successfully Created' % (newModel.name))
        return redirect(url_for('showModels', brand_id=brand_id))
    else:
        return render_template('addModel.html', brand = brand)

#Login

#Disconnect

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)