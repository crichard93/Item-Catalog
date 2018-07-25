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

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///cars.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#Display All Brands
@app.route('/')
@app.route('/brands/')
def showBrands():
    #Retrieve brands object from URL  
    brands = session.query(Brand).order_by(asc(Brand.name))
    return render_template('showBrands.html', brands = brands, login_session = login_session)


#Display all Models in brand with options to add Models
@app.route('/brands/<int:brand_id>/')
def showModels(brand_id):
    #Retrieve brand and model objects from URL  
    brand = session.query(Brand).filter_by(id = brand_id).one()
    models = session.query(Model).filter_by(brand_id = brand_id)
    return render_template('showModels.html', brand = brand, models = models, login_session = login_session)


#Display description + image of Model in a Brand with option to Edit or delete
@app.route('/brands/<int:brand_id>/<int:model_id>/')
def showModel(brand_id, model_id):
    #Retrieve brand and model objects from URL  
    brand = session.query(Brand).filter_by(id = brand_id).one()
    model = session.query(Model).filter_by(id = model_id).one()
    return render_template('showModel.html', brand = brand, model = model, login_session = login_session)


#Edit Model in Brand, first show form, then edit and update database with form data
@app.route('/brands/<int:brand_id>/<int:model_id>/edit/',methods = ('GET', 'POST'))
def editModel(brand_id, model_id):
    #Check login status, redirect to login if not logged in
    if 'username' not in login_session:
        return redirect('/login')
    #Retrieve brand and model objects from URL    
    brand = session.query(Brand).filter_by(id = brand_id).one()
    editModel = session.query(Model).filter_by(id = model_id).one()
    #Check user authority to edit item
    if login_session['user_id'] != editModel.user_id:
        flash('You do not have permission to edit this model.')
        return redirect(url_for('showModels', brand_id = brand_id))
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
@app.route('/brands/<int:brand_id>/<int:model_id>/delete/', methods = ('GET', 'POST'))
def deleteModel(brand_id, model_id):
    #Retrieve brand and model objects from URL  
    brand = session.query(Brand).filter_by(id = brand_id).one()
    model = session.query(Model).filter_by(id = model_id).one()
    #Check user authority to edit item
    if login_session['user_id'] != model.user_id:
        flash('You do not have permission to delete this model.')
        return redirect(url_for('showModels', brand_id = brand_id))
    if request.method == 'POST':
        session.delete(model)
        session.commit()
        return redirect(url_for('showModels', brand_id = brand_id))
    else:
        return render_template('deleteModel.html', brand = brand, model = model, brand_id=brand_id)


#Add Model to Brand. First show the input form, then update database with form data from user
@app.route('/brands/<int:brand_id>/add/', methods = ('GET', 'POST'))
def addModel(brand_id):
    #Check login status, redirect to login if not logged in
    if 'username' not in login_session:
        return redirect('/login')
    #Retrieve brand objects from URL          
    brand = session.query(Brand).filter_by(id = brand_id).one()
    if request.method == 'POST':
        newModel = Model(name = request.form['name'], description = request.form['description'], brand_id = brand_id, user_id = brand.user_id)
        session.add(newModel)
        session.commit()
        flash('New Model %s Successfully Created' % (newModel.name))
        return redirect(url_for('showModels', brand_id=brand_id))
    else:
        return render_template('addModel.html', brand = brand)


# Create randomly generated state token and store in login_session object
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    access_token = login_session.get('access_token')
    return render_template('login.html', STATE=state)


#Login to Google, modified from Udacity provided example
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions, modified from Udacity-provided example
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session, modified from Udacity-provided example
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #Peform HTTP GET request to revoke token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect by deleting login_session details, modified from Udacity-provided example
@app.route('/disconnect')
def disconnect():
    if 'gplus_id' in login_session:
        gdisconnect()
        del login_session['gplus_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        flash("You have successfully been logged out.")
        return redirect(url_for('showBrands'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showBrands'))




if __name__ == '__main__':
    app.secret_key = '123youwi11neve4eve4hackthi5key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)