from flask import Flask, render_template
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	#restaurant = session.query(Restaurant).all()[0]
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
	# output = '<h1><center> %s </center></h1>' %restaurant.name
	# for i in items:
	# 	output += i.name
	# 	output += '</br>'
	# 	output += i.price
	# 	output += '</br>'
	# 	output += i.description
	# 	output += '</br><br>'
	# return output
	return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/new')
def newMenuItem(restaurant_id):
	pass
	
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id):
	pass

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id):
	pass

if __name__ == '__main__':
	app.debug = True
	app.run(host='localhost', port=8080)