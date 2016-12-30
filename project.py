from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#Making an API Endpoint (Get Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def RestaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def MenuIdJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItem=item.serialize)
#------------------------------

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
	return render_template('menu.html', restaurant=restaurant, items=items) #object




@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], restaurant_id=restaurant_id) #variable
		session.add(newItem)
		session.commit()
		flash("New Menu Item Created!!")
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant_id=restaurant_id)
	


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		temp = request.form['edit']
		if temp != '':
			item.name = temp
			session.add(item)
			session.commit()
			flash("Menu Item has been edited!!")
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=item)



@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		
		# name = request.form.to_dict()
		# if name['Cancel'] == 'Cancel':
		# 	return "ohh yess"

		name = request.form.getlist('Delete')
		# if name[0] == 'Delete':
		if len(name) == 1:
			session.delete(item)
			session.commit()
			flash("Menu Item has been deleted!!")
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=item)



if __name__ == '__main__':
	app.secret_key = 'mai_nahi_batata'
	app.debug = True
	app.run(host='localhost', port=8080)