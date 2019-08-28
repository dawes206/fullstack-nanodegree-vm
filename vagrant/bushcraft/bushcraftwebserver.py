#!/usr/bin/python3

#Next thing you're working on is edit menu item and delte menu item. Then you should be done with this iteration in the lesson

#Next thing I need to do is figure out how to sign out of google, that way I can test, step by step, what lorenzo is doing. What I want to test next is that the ajax call is working properly, by making a console.log, or similar, in the gconnect section of this file.

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database_setup import Base, User, Items
# engine = create_engine("sqlite:///bushcrafting.db")
# Base.metadata.bind = create_engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()


from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
app = Flask(__name__)
app.secret_key = 'super_secret_key'


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Items

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client import client
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///bushcrafting.db')
Base.metadata.bind = create_engine
#
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Fake User
user1 = {'name': 'Silas', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1', 'description':'good crab'}, {'name':'Blue Burgers', 'id':'2', 'description':'great burger'},{'name':'Taco Hut', 'id':'3', 'description':'best tacos'}]
# restaurants = []
#
#Fake Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item1 =  {'name':'Silky Saw','description':'good saw','price':'$45','weight' :'8'}

manualID = 1

# items = []

@app.route('/')
def home():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    # return "current session is %s" %login_session["state"]
    return render_template('welcome.html', STATE = state)
    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()
    # restaurants = session.query(Restaurant).all()
    # if not restaurants:
    #     return "No restaurants in database"
    # else:
    #     return render_template('home.html', restaurants = restaurants)

@app.route('/mygear')
def showGear():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    items = session.query(Items).filter_by(user_id=manualID).all()
    return render_template('mygear.html', items = items)
@app.route('/mypack')
def showPack():
    return render_template('mypack.html')

@app.route('/mygear/edit')
def editGear():
    return render_template('mypackedit.html')

@app.route('/<int:itemID>/edit')
def editItem(itemID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Items).filter_by(user_id=manualID, id=itemID).all()
    return render_template('itemedit.html', item = item)

@app.route('/gconnect', methods=['POST'])
def googleLogin():
    if request.args.get('state') != login_session['state']: #check and see if the session state originally assigned to the user is the same as what we're getting from this login request
        output = "<h1>didn't works</h1>"
        response = make_response(json.dumps('invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application.json'
        return response

    credentials = client.credentials_from_clientsecrets_and_code('client_secrets.json',
    ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
    request.data)
    print("------------------access_token-------------------", credentials.access_token)
    # http_auth = credentials.authorize(httplib2.Http())
    # drive_service = discovery.build('drive', 'v3', http=http_auth)
    # appfolder = drive_service.files().get(fileId='appfolder').execute()

    print("------------------data-------------------", request.data.decode('UTF-8'))
    # try:
    # oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='', redirect_uri = 'http://localhost:8080/mygear')
    # credentials = oauth_flow.step2_exchange(code)
    # except FlowExchangeError:
    #     response = make_response(json.dumps('failed to get auth code'), 401)
    #     response.headers['Content-Type'] = 'application.json'
    #     return response

    url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % credentials.access_token
    h = httplib2.Http()
    result = json.loads(h.request(url)[1].decode('UTF-8'))
    print("------------------request-------------------", h.request(url))
    print("--------------------------------------------", result)
    print("----------------resultError-----------------", result.get('error'))

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application.json'
        return response
    output = "<h1>%s</h1>" % credentials.access_token
    response = make_response(json.dumps({'success':True}), 200)
    response.headers['Content-Type'] = 'application.json'
    return response

# @app.route('/<int:restaurantID>/menu')
# def showMenu(restaurantID):
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
#     items = session.query(MenuItem).filter_by(restaurant_id = restaurantID).all()
#     if not items:
#         return render_template('menu.html', restaurant = restaurant, items = items)
#     else:
#         return render_template('menu.html', restaurant = restaurant, items = items)
#
# @app.route('/<int:restaurantID>/edit', methods = ['GET', 'POST'])
# def editRestaurant(restaurantID):
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
#     if request.method == 'POST':
#         restaurant.name = request.form['newName']
#         restaurant.description = request.form['newDesc']
#         restaurant.image = r"/static/"+request.form['newPic']
#         session.add(restaurant)
#         session.commit()
#         return redirect(url_for('home'))
#     else:
#         return render_template('editrestaurant.html', restaurant = restaurant)
#
# @app.route('/<int:restaurantID>/delete', methods = ['GET', 'POST'])
# def deleteRestaurant(restaurantID):
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
#     if request.method == 'POST':
#         session.delete(restaurant)
#         session.commit()
#         return redirect(url_for('home'))
#     else:
#         return render_template('deleterestaurant.html',  restaurant = restaurant)
#
# @app.route('/addrestaurant', methods = ['GET', 'POST'])
# def addRestaurant():
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     if request.method == 'POST':
#         newRestaurant = Restaurant(name = request.form['newName'], description = request.form['newDesc'])
#         session.add(newRestaurant)
#         session.commit()
#         return redirect(url_for('home'))
#     else:
#         return render_template('addrestaurant.html')
#
# @app.route('/<int:restaurantID>/menu/<int:itemID>/edit', methods = ['GET', 'POST'])
# def editMenuItem(restaurantID,itemID):
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
#     item = session.query(MenuItem).filter_by(id = itemID).one()
#     if request.method == 'POST':
#         item.name = request.form['newName']
#         item.price = request.form['newPrice']
#         item.description = request.form['newDesc']
#         session.add(item)
#         session.commit()
#         return redirect(url_for('showMenu',restaurantID = restaurant.id))
#     else:
#         return render_template('editmenuitem.html', restaurant = restaurant, item = item)
#
# @app.route('/<int:restaurantID>/menu/<int:itemID>/delete', methods = ['GET', 'POST'])
# def deleteMenuItem(restaurantID,itemID):
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
#     item = session.query(MenuItem).filter_by(id=itemID).one()
#     if request.method == 'POST':
#         session.delete(item)
#         session.commit()
#         return redirect(url_for('showMenu',restaurantID = restaurant.id))
#     else:
#         return render_template('deletemenuitem.html', restaurant = restaurant, item = item)
#
# @app.route('/<int:restaurantID>/menu/addnewitem', methods = ['GET', 'POST'])
# def addMenuItem(restaurantID):
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
#     if request.method == 'POST':
#         newItem = MenuItem(name = request.form['newName'], price = request.form['newPrice'], description = request.form['newDesc'], restaurant_id = restaurantID)
#         session.add(newItem)
#         session.commit()
#         return redirect(url_for('showMenu', restaurantID = restaurantID))
#     else:
#         return render_template('newmenuitem.html', restaurant = restaurant)
#
# @app.route('/JSON')
# def getRestaurantsJSON():
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     restaurants = session.query(Restaurant).all()
#     return jsonify([rest.serialize for rest in restaurants])
#
# @app.route('/<int:restaurantID>/menu/JSON')
# def getMenuJSON(restaurantID):
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     items = session.query(MenuItem).filter_by(restaurant_id = restaurantID).all()
#     return jsonify([i.serialize for i in items])
# @app.route('/<int:restaurantID>/menu/<int:itemID>/JSON')
# def getItemJSON(restaurantID,itemID):
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     item = session.query(MenuItem).filter_by(id = itemID).one()
#     return jsonify(item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    # app.config["SECRET_KEY"] = 'super_secret_key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
