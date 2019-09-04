#!/usr/bin/python3

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

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def home():
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
    #Displaying query result with group_by parameter means I am unable to access Items.serialize. Create serialize function to serialize results of pack_info
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
    return render_template('welcome.html', STATE = state)

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
    user_info = session.query(User).filter(User.id == userID).first()
    if userID == login_session.get('manualID'):
        loggedUser = True
    else:
        loggedUser = False
    data = {
        'totalWeight' : totalWeight,
        'totalVolume' : totalVolume,
        'catDict' : catDict,
        'loggedUser' : loggedUser,
        'userID' : userID
    }
    return render_template('mypack.html', data=data, user_info = user_info)

@app.route('/<int:userID>/mypack/json')
def showPackJson(userID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    items = session.query(Items).filter(Items.user_id==userID, Items.packed==True).all()
    return jsonify([item.serialize for item in items ])

@app.route('/<int:userID>/mypack/<int:itemID>')
def showItem(userID, itemID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Items).filter(Items.id == itemID).first()
    return render_template('itemshow.html', item = item)

@app.route('/<int:userID>/mygear', methods=['GET', 'POST'])
def showGear(userID):
    if 'manualID' not in login_session:
        return redirect(url_for("login"))
    elif userID is not login_session.get('manualID'):
        return "You are trying to access someone else's stuff"
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method=='POST':
        entries = request.form #<--returns immutable mutli-dict, which will still accept the "in" conditional statement
        packedItems = session.query(Items).filter(Items.id.in_(entries), Items.user_id==login_session.get('manualID')).all()
        unpackedItems = session.query(Items).filter(Items.id.notin_(entries), Items.user_id==login_session.get('manualID')).all()
        user = session.query(User).filter(User.id==userID).first()
        for i in packedItems:
            i.packed = True
            session.add(i)
        for i in unpackedItems:
            i.packed = False
            session.add(i)
        user.pack_name = request.form['pack_name']
        user.pack_description = request.form['pack_description']
        session.add(user)
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
    packInfo = session.query(User).filter(User.id == userID).first()
    data = {
        'totalWeight' : totalWeight,
        'totalVolume' : totalVolume,
        'catDict' : catDict,
        'userID' : userID
    }
    return render_template('mygear.html', data = data, packInfo=packInfo)

@app.route('/<int:userID>/mypack/<int:itemID>/edit', methods=['GET', 'POST'])
def editItem(userID, itemID):
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
        return redirect(url_for('showGear', userID = userID))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Items).filter_by(user_id=login_session.get('manualID'), id=itemID).all()
    categories = session.query(Items.category).filter_by(user_id=login_session.get('manualID')).group_by(Items.category).all()
    catList = list(map(lambda x: x[0], categories))
    if not item:
        return "trying to access someone elses stuff"
    return render_template('itemedit.html', item = item, categories=catList, userID=userID)

@app.route('/<int:userID>/mypack/<int:itemID>/json')
def itemJson(userID, itemID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Items).filter(Items.id==itemID).first()
    return jsonify(item.serialize)

@app.route('/<int:userID>/mypack/<int:itemID>/delete', methods=['GET', 'POST'])
def deleteItem(userID, itemID):
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
        return redirect(url_for("showGear", userID = userID))
    return render_template('deleteItem.html', userID = userID, item=item)

@app.route('/<int:userID>/mypack/additem', methods=['GET','POST'])
def addItem(userID):
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
        return redirect(url_for("showGear", userID = userID))
    categories = session.query(Items.category).filter_by(user_id=login_session.get('manualID')).group_by(Items.category).all()
    catList = list(map(lambda x: x[0], categories))
    return render_template('additem.html', categories=catList, userID = userID)

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
        response = make_response(json.dumps('Certified client_ID does not match app client_ID'), 500)
        response.headers['Content-Type'] = 'application.json'
        return response


    #Check if user already loged in
    if login_session.get('access_token') == 3 and login_session.get('gplus_id') == credentials.id_token['sub']: #<--------changed to prevent error whyile ts. change is not None to is 3
        response = make_response(json.dumps('current user already connected'), 200)
        response.headers['Content-Type'] = 'application.json'
        return response

    #add session info to session
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = credentials.id_token['sub']

    userInfoResponse = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
        {'access_token': login_session['access_token'], 'alt': 'json'}).json()

    #add user to databse
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    #check if new user
    user = session.query(User).filter(User.email==userInfoResponse['email']).first()
    if user:
        response = make_response(json.dumps({'success':True}), 200)
        response.headers['Content-Type'] = 'application.json'
        login_session['manualID'] = user.id
        return userInfoResponse['given_name']

    newUser = User()
    newUser.name = userInfoResponse['given_name']
    newUser.email = userInfoResponse['email']
    session.add(newUser)
    session.commit()
    login_session['manualID'] = newUser.id
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
        return "failed to log off"
    del login_session['access_token']
    del login_session['manualID']
    del login_session['gplus_id']
    del login_session['state']
    return "successfully logged off"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    # app.config["SECRET_KEY"] = 'super_secret_key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
