from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = create_engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1', 'description':'good crab'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1', 'description':'good crab'}, {'name':'Blue Burgers', 'id':'2', 'description':'great burger'},{'name':'Taco Hut', 'id':'3', 'description':'best tacos'}]
# restaurants = []

#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

# items = []

@app.route('/')
def home():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    if not restaurants:
        return "No restaurants in database"
    else:
        return render_template('home.html', restaurants = restaurants)

@app.route('/<int:restaurantID>/menu')
def showMenu(restaurantID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurantID).all()
    if not items:
        return "No menu items in database"
    else:
        return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/<int:restaurantID>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurantID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
    if request.method == 'POST':
        restaurant.name = request.form['newName']
        restaurant.description = request.form['newDesc']
        session.add(restaurant)
        session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('editrestaurant.html', restaurant = restaurant)

@app.route('/<int:restaurantID>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurantID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit
        return redirect(url_for('home'))
    else:
        return render_template('deleterestaurant.html',  restaurant = restaurant)

@app.route('/addrestaurant', methods = ['GET', 'POST'])
def addRestaurant():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['newName'], description = request.form['newDesc'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('addrestaurant.html')

@app.route('/<int:restaurantID>/menu/<int:itemID>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurantID,itemID):
    return render_template('editmenuitem.html', restaurant = restaurant, item = item)

@app.route('/<int:restaurantID>/menu/<int:itemID>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurantID,itemID):
    return render_template('deletemenuitem.html', restaurant = restaurant, item = item)

@app.route('/<int:restaurantID>/menu/addnewitem', methods = ['GET', 'POST'])
def addMenuItem(restaurantID):
    return render_template('newmenuitem.html', restaurant = restaurant)
