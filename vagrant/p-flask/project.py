#!/etc python3
from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = create_engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurant/<int:restaurantID>/')
def restaurantMenu(restaurantID):
    restaurant = session.query(Restaurant).filter_by(id = restaurantID).first()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurantID)
    output = ''
    for i in items:
        output += i.name
        output+= '</br>'
        output += i.price
        output+= '</br>'
        output += i.description
        output+= '</br>'
        output+= '</br>'
    return output

@app.route('/restaurant/<int:restaurantID>/new/')
def newMenuItem(restaurantID):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurantID>/<int:menuID>/edit/')
def editMenuItem(restaurantID, menuID):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurantID>/<int:menuID>/delete/')
def deleteMenuItem(restaurantID, menuID):
    return "page to delete a menu item. Task 3 complete!"



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
