#Python code to communicate with database
#Will run sqllite

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = create_engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# restaurantExample = Restaurant(name='')
# session.add(restaurantExample)
# session.commit()
#tables -> engine.table_names()
#tables: menu_item, restaurant
#tables: MenuItem, Restaurant

def addRestaurant(name):
    newRestaurant = Restaurant(name=name)
    session.add(newRestaurant)
    session.commit()

def testFunc():
    #print('success')
    return('success')

def getRestaurantNames():
    restaurantList = session.query(Restaurant).all()
    restaurantNames = map(lambda x: x.name, restaurantList)
    return list(restaurantNames)
