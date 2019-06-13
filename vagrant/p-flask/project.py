#!/etc python3
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app.secret_key = 'super_secret_key'

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = create_engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurant/<int:restaurantID>/')
def restaurantMenu(restaurantID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurantID).first()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurantID)
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurant/<int:restaurantID>/new/', methods = ['POST','GET'])
def newMenuItem(restaurantID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurantID).first()
    if request.method == 'GET':
        return render_template('newmenuitem.html', restaurant = restaurant)
    else:
        newItem = MenuItem(name = request.form['newItem'], restaurant_id = restaurantID)
        # return 'hello'
        session.add(newItem)
        session.commit()
        flash('new menu item created')
        return redirect(url_for('restaurantMenu', restaurantID = restaurant.id))

# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurantID>/<int:menuID>/edit/', methods = ['GET','POST'])
def editMenuItem(restaurantID, menuID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurantID).first()
    item = session.query(MenuItem).filter_by(id = menuID).one()
    if request.method == 'GET':
        return render_template('editmenuitem.html', restaurant = restaurant, item = item)
    else:
        item.name = request.form['newName']
        # return '{}'.format(item.name)
        session.add(item)
        session.commit()
        flash('menu item edited')
        return redirect(url_for('restaurantMenu', restaurantID = restaurant.id))
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurantID>/<int:menuID>/delete/', methods = ['GET','POST'])
def deleteMenuItem(restaurantID, menuID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(MenuItem).filter_by(id = menuID).one()
    if request.method == 'GET':
        return render_template('deletemenuitem.html', item = item)
    else:
        session.delete(item)
        session.commit()
        flash('menu item deleted')
        return redirect(url_for('restaurantMenu', restaurantID = restaurantID))

@app.route('/restaurant/<int:restaurantID>/menu/JSON/')
def restaurantMenuJSON(restaurantID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurantID).first()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurantID)
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurantID>/menu/<int:menuID>/JSON/')
def menuItemJson(restaurantID, menuID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurantID).first()
    item = session.query(MenuItem).filter_by(id = menuID).one()
    return jsonify(item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
