from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<string:restaurantName>/menu')
def showMenu(restaurantName):
    return render_template('menu.html')

@app.route('/<string:restaurantName>/edit')
def editRestaurant(restaurantName):
    return render_template('editrestaurant.html')

@app.route('/<string:restaurantName>/delete')
def deleteRestaurant(restaurantName):
    return render_template('deleterestaurant.html')

@app.route('/addrestaurant')
def addRestaurant():
    return render_template('addrestaurant.html')

@app.route('/<string:restaurantName>/menu/<int:itemID>/edit')
def editMenuItem(restaurantName,itemID):
    return render_template('editmenuitem.html')

@app.route('/<string:restaurantName>/menu/<int:itemID>/delete')
def deleteMenuItem(restaurantName,itemID):
    return render_template('deletemenuitem.html')

@app.route('/<string:restaurantName>/menu/addnewitem')
def AddMenuItem(restaurantName):
    return render_template('newmenuitem.html')
