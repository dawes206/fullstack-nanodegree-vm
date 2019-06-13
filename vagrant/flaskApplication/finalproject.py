from flask import Flask, render_template, request, redirect
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
    if not restaurants:
        return "No restaurants in database"
    else:
        return render_template('home.html', restaurants = restaurants)

@app.route('/<string:restaurantName>/menu')
def showMenu(restaurantName):
    if not items:
        return "No menu items in database"
    else:
        return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/<string:restaurantName>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurantName):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(name = restaurantName).one()
    if request.method == 'POST':
        restaurant.name = request.form['newName']
        restaurant.description = request.form['newDesc']
        session.add(restaurant)
        session.commit()
        return redirect(url_for(home))
    else:
        return render_template('editrestaurant.html', restaurant = restaurant)

@app.route('/<string:restaurantName>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurantName):
    return render_template('deleterestaurant.html',  restaurant = restaurant)

@app.route('/addrestaurant')
def addRestaurant():
    return render_template('addrestaurant.html', methods = ['GET', 'POST'])

@app.route('/<string:restaurantName>/menu/<int:itemID>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurantName,itemID):
    return render_template('editmenuitem.html', restaurant = restaurant, item = item)

@app.route('/<string:restaurantName>/menu/<int:itemID>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurantName,itemID):
    return render_template('deletemenuitem.html', restaurant = restaurant, item = item)

@app.route('/<string:restaurantName>/menu/addnewitem', methods = ['GET', 'POST'])
def addMenuItem(restaurantName):
    return render_template('newmenuitem.html', restaurant = restaurant)
