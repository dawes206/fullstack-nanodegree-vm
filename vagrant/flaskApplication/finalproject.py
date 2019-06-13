from flask import Flask, render_template
app = Flask(__name__)

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1', 'description':'good crab'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1', 'description':'good crab'}, {'name':'Blue Burgers', 'id':'2', 'description':'great burger'},{'name':'Taco Hut', 'id':'3', 'description':'best tacos'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

@app.route('/')
def home():
    return render_template('home.html', restaurants = restaurants)

@app.route('/<string:restaurantName>/menu')
def showMenu(restaurantName):
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/<string:restaurantName>/edit')
def editRestaurant(restaurantName):
    return render_template('editrestaurant.html', restaurant = restaurant)

@app.route('/<string:restaurantName>/delete')
def deleteRestaurant(restaurantName):
    return render_template('deleterestaurant.html',  restaurant = restaurant)

@app.route('/addrestaurant')
def addRestaurant():
    return render_template('addrestaurant.html')

@app.route('/<string:restaurantName>/menu/<int:itemID>/edit')
def editMenuItem(restaurantName,itemID):
    return render_template('editmenuitem.html', item = item)

@app.route('/<string:restaurantName>/menu/<int:itemID>/delete')
def deleteMenuItem(restaurantName,itemID):
    return render_template('deletemenuitem.html', item = item)

@app.route('/<string:restaurantName>/menu/addnewitem')
def AddMenuItem(restaurantName):
    return render_template('newmenuitem.html')
