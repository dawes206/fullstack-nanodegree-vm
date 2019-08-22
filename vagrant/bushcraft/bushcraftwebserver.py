#Next thing you're working on is edit menu item and delte menu item. Then you should be done with this iteration in the lesson

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database_setup import Base, User, Items
# engine = create_engine("sqlite:///bushcrafting.db")
# Base.metadata.bind = create_engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()


from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Items

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
    return render_template('welcome.html')
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
