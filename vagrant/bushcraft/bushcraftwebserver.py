#!/usr/bin/python3

#Next thing you're working on is edit menu item and delte menu item. Then you should be done with this iteration in the lesson

#Next thing I need to do is figure out how to sign out of google, that way I can test, step by step, what lorenzo is doing. What I want to test next is that the ajax call is working properly, by making a console.log, or similar, in the gconnect section of this file.

# from sqlalchemy import create_engine, text, func
# from sqlalchemy.orm import sessionmaker
# from database_setup import Base, User, Items
# engine = create_engine("sqlite:///bushcrafting.db")
# Base.metadata.bind = create_engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()


from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
app = Flask(__name__)
app.secret_key = 'super_secret_key'


from sqlalchemy import create_engine, func
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

# items = []

@app.route('/')
def home():
    # if 'manualID' not in login_session:
    #     return redirect(url_for("login"))
    # return "current session is %s" %login_session["state"]
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    users = session.query(User).all()
    if 'manualID' in login_session:
        loggedIn = True
    else:
        loggedIn = False
    return render_template('allpacks.html', users = users, loggedIn = loggedIn)

@app.route('/allPacksJson')
def getPacksJson():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    pack_info = session.query(User.pack_name, User.pack_description, func.sum(Items.weight).label('Total_Weight(Oz)'), func.sum(Items.volume).label('Total_Volume(L)')).join(Items).filter(Items.packed==True).group_by(Items.user_id).all()
    def serialize(pack):
        dictionary = {}
        for key in pack.keys():
            dictionary[key] = getattr(pack, key)
        return dictionary
    return jsonify([serialize(pack) for pack in pack_info])

@app.route('/login')
def login():
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

@app.route('/mygear', methods=['GET', 'POST'])
def showGear():
    if 'manualID' not in login_session:
        return redirect(url_for("login"))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # items = session.query(Items).filter_by(user_id=manualID).all()
    if request.method=='POST':
        entries = request.form #<--returns immutable mutli-dict, which will still accept the "in" conditional statement
        packedItems = session.query(Items).filter(Items.id.in_(entries), Items.user_id==login_session.get('manualID')).all()
        unpackedItems = session.query(Items).filter(Items.id.notin_(entries), Items.user_id==login_session.get('manualID')).all()
        for i in packedItems:
            i.packed = True
            session.add(i)
        for i in unpackedItems:
            i.packed = False
            session.add(i)
        session.commit()
        return redirect(url_for('showPack', userID = login_session.get('manualID')))

    catDict = {}
    categories = session.query(Items.category).filter(Items.user_id==login_session.get('manualID')).group_by(Items.category).all()
    for i in categories:
        catDict[i.category] = session.query(Items).filter_by(
        user_id=login_session.get('manualID'),
        category=i.category
        ).all()

    totalWeight = session.query(func.sum(Items.weight).label('totalWeight')).filter(Items.weight,Items.user_id==login_session.get('manualID')).first().totalWeight
    totalVolume = session.query(func.sum(Items.volume).label('totalVol')).filter(Items.volume,Items.user_id==login_session.get('manualID')).first().totalVol
    data = {
        # 'items': items,
        'totalWeight' : totalWeight,
        'totalVolume' : totalVolume,
        'catDict' : catDict
    }
    return render_template('mygear.html', data = data)

@app.route('/<int:userID>/mypack')
def showPack(userID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    catDict = {}
    categories = session.query(Items.category).filter(Items.user_id==userID, Items.packed==True).group_by(Items.category).all()
    for i in categories:
        catDict[i.category] = session.query(Items).filter_by(
        user_id= userID,
        category=i.category,
        packed=True
        ).all()
    totalWeight = session.query(func.sum(Items.weight).label('totalWeight')).filter(Items.weight,Items.user_id==userID, Items.packed==True).first().totalWeight
    totalVolume = session.query(func.sum(Items.volume).label('totalVol')).filter(Items.volume,Items.user_id==userID, Items.packed==True).first().totalVol
    print('-----------------------', categories)
    if userID == login_session.get('manualID'):
        loggedUser = True
    else:
        loggedUser = False
    data = {
        # 'items': items,
        'totalWeight' : totalWeight,
        'totalVolume' : totalVolume,
        'catDict' : catDict,
        'loggedUser' : loggedUser
    }
    return render_template('mypack.html', data=data)

@app.route('/<int:userID>/mypack/json')
def showPackJson(userID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    items = session.query(Items).filter(Items.user_id==userID, Items.packed==True).all()
    return jsonify([item.serialize for item in items ])


@app.route('/mygear/edit')
def editGear():
    if 'manualID' not in login_session:
        return redirect(url_for("login"))
    return render_template('mypackedit.html')

@app.route('/<int:itemID>/edit', methods=['GET', 'POST'])
def editItem(itemID):
    if 'manualID' not in login_session:
        return redirect(url_for("login"))
    if request.method == 'POST':
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        item = session.query(Items).filter_by(id=itemID,user_id = login_session['manualID']).first()
        item.name = request.form['updateName'].lower()
        item.description = request.form['updateDescription'].lower()
        item.amount = request.form['updateAmount'].lower()
        item.weight = request.form['updateWeight'].lower()
        item.volume = request.form['updateVolume'].lower()
        if "updateCategory" not in request.form or (request.form['updateCategory']=='newCategory' and request.form["newCategoryValue"]==''):
            item.category = 'none'
        elif request.form['updateCategory'] == 'newCategory':
            item.category = request.form["newCategoryValue"].lower()
        else:
            item.category = request.form['updateCategory'].lower()
        session.add(item)
        session.commit()
        return redirect(url_for('showGear'))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Items).filter_by(user_id=login_session.get('manualID'), id=itemID).all()
    categories = session.query(Items.category).filter_by(user_id=login_session.get('manualID')).group_by(Items.category).all()
    catList = list(map(lambda x: x[0], categories))
    if not item:
        return "trying to access someone elses stuff"
    return render_template('itemedit.html', item = item, categories=catList)

@app.route('/<int:itemID>/delete', methods=['GET', 'POST'])
def deleteItem(itemID):
    if 'manualID' not in login_session:
        return redirect(url_for("login"))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Items).filter(Items.id==itemID, Items.user_id==login_session.get('manualID')).first()
    if not item:
        return "trying to access someone elses stuff"
    if request.method=='POST':
        session.delete(item)
        session.commit()
        return redirect(url_for("showGear"))
    return render_template('deleteItem.html', item=item)

@app.route('/additem', methods=['GET','POST'])
def addItem():
    if 'manualID' not in login_session:
        return redirect(url_for("login"))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newItem = Items()
        newItem.name = request.form["name"].lower()
        newItem.description = request.form["description"].lower()
        newItem.amount = request.form["amount"].lower()
        newItem.weight = request.form["weight"].lower()
        newItem.volume = request.form["volume"].lower()
        if "category" not in request.form or (request.form['category']=='newCategory' and request.form["newCategoryValue"]==''):
            newItem.category = 'none'
        elif request.form["category"] == 'newCategory':
            newItem.category = request.form["newCategoryValue"].lower()
        else:
            newItem.category = request.form["category"].lower()
        newItem.user_id = login_session.get('manualID')
        session.add(newItem)
        session.commit()
        return redirect(url_for("showGear"))
    categories = session.query(Items.category).filter_by(user_id=login_session.get('manualID')).group_by(Items.category).all()
    catList = list(map(lambda x: x[0], categories))
    return render_template('additem.html', categories=catList)

@app.route('/gconnect', methods=['POST'])
def googleLogin():
    # #Adding to avoid proxy#
    # response = make_response(json.dumps({'success':True}), 200)
    # response.headers['Content-Type'] = 'application.json'
    # return response
    # ########
    if request.args.get('state') != login_session['state']: #check and see if the session state originally assigned to the user is the same as what we're getting from this login request
        output = "<h1>didn't works</h1>"
        response = make_response(json.dumps('invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application.json'
        return response

    credentials = client.credentials_from_clientsecrets_and_code('client_secrets.json',
    ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
    request.data)
    print("------------------id_token-------------------", credentials.id_token)
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
    resultAPICert = json.loads(h.request(url)[1].decode('UTF-8'))

    if resultAPICert.get('error') is not None:
        response = make_response(json.dumps(resultAPICert.get('error')), 500)
        response.headers['Content-Type'] = 'application.json'
        return response

    if resultAPICert['user_id'] != credentials.id_token['sub']:
        response = make_response(json.dumps('Token user does not match certified api'), 500)
        response.headers['Content-Type'] = 'application.json'
        return response

    if resultAPICert['issued_to'] != CLIENT_ID:
        print("----------HOT DOG----------------------")
        response = make_response(json.dumps('Certified client_ID does not match app client_ID'), 500)
        response.headers['Content-Type'] = 'application.json'
        return response


    #Check if user already loged in
    if login_session.get('access_token') == 3 and login_session.get('gplus_id') == credentials.id_token['sub']: #<--------changed to prevent error whyile ts. change is not None to is 3
        print ("----------------login_+session access--------------", login_session.get('access_token'))
        response = make_response(json.dumps('current user already connected'), 200)
        response.headers['Content-Type'] = 'application.json'
        return response

    print("------------------request-------------------", h.request(url))
    print("--------------------------------------------", resultAPICert['user_id'])
    print("----------------resultAPICertError-----------------", resultAPICert.get('error'))

    #add session info to session
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = credentials.id_token['sub']

    userInfoResponse = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
        {'access_token': login_session['access_token'], 'alt': 'json'}).json()

    print("----------------user_info-----------", userInfoResponse)
    print("----------------user name-----------", userInfoResponse['given_name'])

    #add user to databse
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    #check if new user
    user = session.query(User).filter(User.email==userInfoResponse['email']).first()
    if user:
        response = make_response(json.dumps({'success':True}), 200)
        response.headers['Content-Type'] = 'application.json'
        login_session['manualID'] = user.id
        print("----------------not new-----------")
        print('----------------lgin session----------', login_session.get('manualID'))
        return userInfoResponse['given_name']

    newUser = User()
    newUser.name = userInfoResponse['given_name']
    newUser.email = userInfoResponse['email']
    session.add(newUser)
    session.commit()
    login_session['manualID'] = newUser.id
    print('----------------lgin session----------', login_session.get('manualID'))
    response = make_response(json.dumps({'success':True}), 200)
    response.headers['Content-Type'] = 'application.json'
    return userInfoResponse['given_name']

@app.route('/gdisconnect', methods = ["GET"])
def gdisconnect():
    if 'manualID' not in login_session:
        return redirect(url_for("login"))
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token'] #<------added 1 at end of url because I don't want to revoke token during ts
    h = httplib2.Http()
    disconnectResponse = json.loads(h.request(url)[1].decode('UTF-8'))
    if disconnectResponse.get('error'):
        print('-----------------reason-------------', disconnectResponse)
        print('------------------login_session token-----------', login_session['access_token'])
        return "failed to log off"
    del login_session['access_token']
    del login_session['manualID']
    del login_session['gplus_id']
    del login_session['state']
    if 'access_token' not in login_session:
        print('------------------access_token gone-----------')
    return "successfully logged off"

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
